"""
Bot Qualificador de Leads - Universal
=====================================
Um unico bot que se adapta a QUALQUER nicho.

Suporta dois MODOS:
- 'fixo': fluxo de perguntas pre-definidas (rapido, sem custo, sem IA)
- 'ia':   conversa natural com LLM (Groq) usando o cerebro do consultor

O modo e definido no campo BOT_CONFIG['modo'] do arquivo de config.
"""

import os
import json
import logging
import importlib
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# --------------------------------------------------------------------
# CARREGAMENTO DE .env
# --------------------------------------------------------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DONO_CHAT_ID = os.getenv("DONO_CHAT_ID")
NICHO = os.getenv("NICHO", "corretor")
CLIENTE_ENV = os.getenv("CLIENTE")  # opcional: sobrescreve cliente_default do config

# --------------------------------------------------------------------
# CARREGAMENTO DA CONFIG DE NICHO
# --------------------------------------------------------------------
try:
    modulo_config = importlib.import_module(f"configs.{NICHO}")
    BOT_CONFIG = modulo_config.BOT_CONFIG
except ModuleNotFoundError:
    raise SystemExit(
        f"Configuracao 'configs/{NICHO}.py' nao encontrada. "
        f"Verifique a variavel NICHO no .env"
    )

MODO = BOT_CONFIG.get("modo", "fixo")

# --------------------------------------------------------------------
# CARREGAMENTO DO PERFIL DE CLIENTE (apenas modo IA)
# --------------------------------------------------------------------
CLIENTE = None
if MODO == "ia":
    nome_cliente = CLIENTE_ENV or BOT_CONFIG.get("cliente_default", "direcional_israel")
    try:
        modulo_cliente = importlib.import_module(f"clientes.{nome_cliente}")
        CLIENTE = modulo_cliente.CLIENTE
    except ModuleNotFoundError:
        raise SystemExit(
            f"Perfil de cliente 'clientes/{nome_cliente}.py' nao encontrado. "
            f"Verifique a variavel CLIENTE no .env ou o cliente_default no config."
        )

    # Importa o motor de IA apenas se estivermos em modo IA
    from ai_engine import (
        conversar_com_lead,
        extrair_dados_do_lead,
        lead_esta_completo,
        contar_campos_preenchidos,
        montar_system_prompt,
    )

    SYSTEM_PROMPT = montar_system_prompt(
        BOT_CONFIG["system_prompt_template"],
        CLIENTE,
    )

# --------------------------------------------------------------------
# LOGGING
# --------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------
# PASTA DE LEADS
# --------------------------------------------------------------------
LEADS_DIR = Path("leads")
LEADS_DIR.mkdir(exist_ok=True)

# Estados da conversa
PERGUNTANDO = 0   # modo fixo
CONVERSANDO = 1   # modo IA


# ====================================================================
# HANDLERS COMPARTILHADOS
# ====================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ponto de entrada. Decide o modo e delega."""
    if MODO == "ia":
        return await start_ia(update, context)
    return await start_fixo(update, context)


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela a conversa em qualquer modo."""
    await update.message.reply_text(
        "Tudo bem! Quando quiser, e so digitar /start novamente.",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos:\n"
        "/start - Comecar (ou reiniciar) o atendimento\n"
        "/cancelar - Cancelar o atendimento atual\n"
        "/ajuda - Ver esta mensagem"
    )


# ====================================================================
# MODO FIXO (fluxo de perguntas pre-definidas)
# ====================================================================
async def start_fixo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["respostas"] = {}
    context.user_data["indice"] = 0

    msg = BOT_CONFIG["mensagem_boas_vindas"].format(empresa=BOT_CONFIG["empresa"])
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())
    return await proxima_pergunta_fixa(update, context)


async def proxima_pergunta_fixa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data["indice"]
    perguntas = BOT_CONFIG["perguntas"]

    if idx >= len(perguntas):
        return await finalizar_fixo(update, context)

    pergunta = perguntas[idx]

    if pergunta.get("opcoes"):
        keyboard = [[KeyboardButton(op)] for op in pergunta["opcoes"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(pergunta["pergunta"], reply_markup=markup)
    else:
        await update.message.reply_text(pergunta["pergunta"], reply_markup=ReplyKeyboardRemove())

    return PERGUNTANDO


async def receber_resposta_fixa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data["indice"]
    perguntas = BOT_CONFIG["perguntas"]
    pergunta = perguntas[idx]
    resposta = (update.message.text or "").strip()

    if pergunta.get("opcoes") and resposta not in pergunta["opcoes"]:
        opcoes = ", ".join(pergunta["opcoes"])
        await update.message.reply_text(f"Por favor, escolha uma das opcoes: {opcoes}")
        return PERGUNTANDO

    context.user_data["respostas"][pergunta["id"]] = resposta
    context.user_data["indice"] += 1
    return await proxima_pergunta_fixa(update, context)


async def finalizar_fixo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respostas = context.user_data["respostas"]
    score = calcular_score(respostas)
    lead = salvar_lead(respostas, score, update.effective_user)
    await notificar_dono(context, lead)

    nome = respostas.get("nome", "")
    telefone = respostas.get("telefone", "informado")
    msg_final = BOT_CONFIG["mensagem_final"].format(
        nome=nome, telefone=telefone, empresa=BOT_CONFIG["empresa"]
    )
    await update.message.reply_text(msg_final, reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


# ====================================================================
# MODO IA (conversa com LLM)
# ====================================================================
async def start_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia conversa em modo IA. Manda a apresentacao inicial do consultor."""
    context.user_data.clear()
    context.user_data["historico"] = []
    context.user_data["dados_coletados"] = {}
    context.user_data["turno"] = 0

    apresentacao = CLIENTE.get(
        "apresentacao_inicial",
        f"Ola! Sou {CLIENTE['nome_consultor']}, consultor da {CLIENTE['nome_imobiliaria']}. Como posso ajudar?",
    )

    # Adiciona a apresentacao ao historico como se a IA tivesse falado
    context.user_data["historico"].append(
        {"role": "assistant", "content": apresentacao}
    )

    await update.message.reply_text(apresentacao, reply_markup=ReplyKeyboardRemove())
    return CONVERSANDO


async def conversar_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler de conversa continua em modo IA."""
    mensagem_usuario = (update.message.text or "").strip()
    if not mensagem_usuario:
        return CONVERSANDO

    # Inicializa se veio sem /start (usuario mandou msg direto)
    if "historico" not in context.user_data:
        return await start_ia(update, context)

    historico = context.user_data["historico"]
    turno = context.user_data.get("turno", 0)

    # Adiciona mensagem do usuario
    historico.append({"role": "user", "content": mensagem_usuario})

    # Chama a IA pra gerar resposta
    await update.message.chat.send_action("typing")
    resposta_ia = conversar_com_lead(historico, SYSTEM_PROMPT)
    historico.append({"role": "assistant", "content": resposta_ia})
    context.user_data["turno"] = turno + 1

    # Envia resposta pro usuario
    await update.message.reply_text(resposta_ia)

    # Periodicamente, extrai dados estruturados da conversa
    extrair_a_cada = BOT_CONFIG.get("extrair_a_cada_turnos", 2)
    if context.user_data["turno"] % extrair_a_cada == 0:
        try:
            dados_novos = extrair_dados_do_lead(
                historico=historico,
                campos=BOT_CONFIG["campos_a_coletar"],
                campos_atuais=context.user_data["dados_coletados"],
            )
            context.user_data["dados_coletados"] = dados_novos
            preenchidos = contar_campos_preenchidos(
                dados_novos, BOT_CONFIG["campos_a_coletar"]
            )
            logger.info(
                f"Extracao (turno {context.user_data['turno']}): "
                f"{preenchidos}/{len(BOT_CONFIG['campos_a_coletar'])} campos"
            )
        except Exception as e:
            logger.error(f"Erro na extracao: {e}")

    # Verifica se ja da pra finalizar
    dados = context.user_data["dados_coletados"]
    if lead_esta_completo(dados, BOT_CONFIG["campos_minimos_para_finalizar"]):
        return await finalizar_ia(update, context)

    # Safety: se passou do maximo, forca finalizacao
    max_turnos = BOT_CONFIG.get("max_turnos", 30)
    if context.user_data["turno"] >= max_turnos:
        logger.warning(f"Atingiu max_turnos ({max_turnos}), finalizando forcado.")
        return await finalizar_ia(update, context)

    return CONVERSANDO


async def finalizar_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Encerra a conversa no modo IA."""
    dados = context.user_data.get("dados_coletados", {})

    # Ultima extracao pra garantir que capturou tudo do final da conversa
    try:
        dados_finais = extrair_dados_do_lead(
            historico=context.user_data["historico"],
            campos=BOT_CONFIG["campos_a_coletar"],
            campos_atuais=dados,
        )
        dados = dados_finais
    except Exception as e:
        logger.error(f"Erro na extracao final: {e}")

    score = calcular_score(dados)
    lead = salvar_lead(dados, score, update.effective_user)
    await notificar_dono(context, lead)

    # Envia mensagem de encerramento
    msg_final = BOT_CONFIG.get(
        "mensagem_final",
        "Otimo! Suas informacoes foram registradas. Em breve entrarei em contato.",
    )
    await update.message.reply_text(msg_final, reply_markup=ReplyKeyboardRemove())

    context.user_data.clear()
    return ConversationHandler.END


# ====================================================================
# SCORING E PERSISTENCIA (compartilhado entre os dois modos)
# ====================================================================
def calcular_score(dados: dict) -> int:
    """Calcula pontuacao baseada no scoring configurado."""
    score = 0
    scoring = BOT_CONFIG.get("scoring", {})
    for campo, mapa_pontos in scoring.items():
        valor = dados.get(campo)
        if not valor:
            continue
        # Compara em minusculas pra ser flexivel
        valor_norm = str(valor).lower().strip()
        for chave, pontos in mapa_pontos.items():
            if chave.lower() in valor_norm or valor_norm in chave.lower():
                score += pontos
                break

    # No modo IA, bonus por completude dos campos
    if MODO == "ia":
        preenchidos = contar_campos_preenchidos(dados, BOT_CONFIG["campos_a_coletar"])
        total = len(BOT_CONFIG["campos_a_coletar"])
        if total > 0:
            score += int((preenchidos / total) * 10)

    return score


def classificar_lead(score: int) -> str:
    if score >= 15:
        return "QUENTE"
    if score >= 8:
        return "MORNO"
    return "FRIO"


def salvar_lead(dados: dict, score: int, user) -> dict:
    """Persiste o lead em JSON."""
    lead = {
        "timestamp": datetime.now().isoformat(),
        "telegram_user_id": user.id,
        "telegram_username": user.username,
        "nicho": BOT_CONFIG["nicho"],
        "modo": MODO,
        "cliente": CLIENTE["nome_imobiliaria"] if CLIENTE else None,
        "score": score,
        "classificacao": classificar_lead(score),
        "dados": dados,
    }

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = LEADS_DIR / f"lead_{stamp}_{user.id}.json"
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lead, f, ensure_ascii=False, indent=2)

    logger.info(f"Lead salvo: {arquivo} | Score: {score} | {lead['classificacao']}")
    return lead


async def notificar_dono(context: ContextTypes.DEFAULT_TYPE, lead: dict):
    """Envia resumo do lead ao dono via Telegram."""
    if not DONO_CHAT_ID:
        logger.warning("DONO_CHAT_ID nao configurado")
        return

    emoji_class = {"QUENTE": "🔥", "MORNO": "☀️", "FRIO": "❄️"}
    emoji = emoji_class.get(lead["classificacao"], "📩")

    texto = f"{emoji} *NOVO LEAD - {lead['classificacao']}*\n"
    texto += f"_Score: {lead['score']} | Nicho: {lead['nicho']} | Modo: {lead['modo']}_\n"
    if lead.get("cliente"):
        texto += f"_Cliente: {lead['cliente']}_\n"
    texto += "\n"

    # Formata os dados coletados
    dados = lead.get("dados", {})
    for campo, valor in dados.items():
        if valor and valor not in ("null", None, ""):
            label = campo.replace("_", " ").title()
            texto += f"*{label}:* {valor}\n"

    if lead.get("telegram_username"):
        texto += f"\n💬 Telegram: @{lead['telegram_username']}"

    try:
        await context.bot.send_message(
            chat_id=DONO_CHAT_ID,
            text=texto,
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Erro ao notificar dono: {e}")


# ====================================================================
# ENTRY POINT
# ====================================================================
def main():
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN nao configurado. Copie .env.example para .env e preencha."
        )

    if MODO == "ia" and not os.getenv("GROQ_API_KEY"):
        raise SystemExit(
            "Modo IA ativo, mas GROQ_API_KEY nao configurada. "
            "Pegue sua chave em https://console.groq.com e adicione no .env"
        )

    app = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler suporta os dois modos via estados diferentes.
    # Entry point unico via /start (evita reset em cada mensagem no modo IA).
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PERGUNTANDO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receber_resposta_fixa),
            ],
            CONVERSANDO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, conversar_ia),
            ],
        },
        fallbacks=[
            CommandHandler("cancelar", cancelar),
            CommandHandler("parar", cancelar),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("ajuda", ajuda))

    logger.info(f"Bot iniciado | Nicho: {BOT_CONFIG['nicho']} | Modo: {MODO}")
    if CLIENTE:
        logger.info(f"Cliente: {CLIENTE['nome_imobiliaria']} ({CLIENTE['nome_consultor']})")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
