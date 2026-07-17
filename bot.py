"""
Bot Qualificador de Leads - Universal
=====================================
Um unico bot que se adapta a QUALQUER nicho via arquivo de configuracao.

Como funciona:
1. Le a variavel NICHO do .env
2. Importa dinamicamente o arquivo configs/<NICHO>.py
3. Roda o fluxo de perguntas definido no config
4. Salva o lead em JSON e notifica o dono via Telegram

Para adaptar a um novo nicho: basta criar um novo arquivo em configs/
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
# CARREGAMENTO DE CONFIG
# --------------------------------------------------------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DONO_CHAT_ID = os.getenv("DONO_CHAT_ID")
NICHO = os.getenv("NICHO", "corretor")

try:
    modulo_config = importlib.import_module(f"configs.{NICHO}")
    BOT_CONFIG = modulo_config.BOT_CONFIG
except ModuleNotFoundError:
    raise SystemExit(
        f"Configuracao 'configs/{NICHO}.py' nao encontrada. "
        f"Verifique a variavel NICHO no seu .env"
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

# Estado unico da conversa
PERGUNTANDO = 0


# ====================================================================
# HANDLERS
# ====================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia a conversa com o lead."""
    context.user_data.clear()
    context.user_data["respostas"] = {}
    context.user_data["indice"] = 0

    msg = BOT_CONFIG["mensagem_boas_vindas"].format(
        empresa=BOT_CONFIG["empresa"]
    )
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())
    return await proxima_pergunta(update, context)


async def proxima_pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a proxima pergunta do fluxo ou finaliza."""
    idx = context.user_data["indice"]
    perguntas = BOT_CONFIG["perguntas"]

    if idx >= len(perguntas):
        return await finalizar(update, context)

    pergunta = perguntas[idx]

    if pergunta.get("opcoes"):
        # Pergunta com botoes de opcao
        keyboard = [[KeyboardButton(op)] for op in pergunta["opcoes"]]
        markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await update.message.reply_text(pergunta["pergunta"], reply_markup=markup)
    else:
        # Pergunta de resposta livre
        await update.message.reply_text(
            pergunta["pergunta"],
            reply_markup=ReplyKeyboardRemove(),
        )

    return PERGUNTANDO


async def receber_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Valida e armazena a resposta, depois avanca."""
    idx = context.user_data["indice"]
    perguntas = BOT_CONFIG["perguntas"]
    pergunta = perguntas[idx]
    resposta = (update.message.text or "").strip()

    # Se a pergunta tem opcoes fixas, valida
    if pergunta.get("opcoes") and resposta not in pergunta["opcoes"]:
        opcoes = ", ".join(pergunta["opcoes"])
        await update.message.reply_text(
            f"Por favor, escolha uma das opcoes: {opcoes}"
        )
        return PERGUNTANDO

    context.user_data["respostas"][pergunta["id"]] = resposta
    context.user_data["indice"] += 1

    return await proxima_pergunta(update, context)


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela a conversa."""
    await update.message.reply_text(
        "Tudo bem! Quando quiser, e so digitar /start novamente.",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


# ====================================================================
# FINALIZACAO E NOTIFICACAO
# ====================================================================
def calcular_score(respostas: dict) -> int:
    """Calcula pontuacao do lead com base no scoring configurado."""
    score = 0
    scoring = BOT_CONFIG.get("scoring", {})
    for campo, mapa_pontos in scoring.items():
        valor = respostas.get(campo)
        if valor and valor in mapa_pontos:
            score += mapa_pontos[valor]
    return score


def classificar_lead(score: int) -> str:
    """Classifica o lead em QUENTE / MORNO / FRIO."""
    if score >= 15:
        return "QUENTE"
    if score >= 8:
        return "MORNO"
    return "FRIO"


def salvar_lead(respostas: dict, score: int, user) -> dict:
    """Persiste o lead em JSON e devolve o dict completo."""
    lead = {
        "timestamp": datetime.now().isoformat(),
        "telegram_user_id": user.id,
        "telegram_username": user.username,
        "nicho": BOT_CONFIG["nicho"],
        "score": score,
        "classificacao": classificar_lead(score),
        "respostas": respostas,
    }

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = LEADS_DIR / f"lead_{stamp}_{user.id}.json"
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lead, f, ensure_ascii=False, indent=2)

    logger.info(f"Lead salvo: {arquivo} | Score: {score} | {lead['classificacao']}")
    return lead


async def notificar_dono(context: ContextTypes.DEFAULT_TYPE, lead: dict):
    """Envia resumo do lead para o dono via Telegram."""
    if not DONO_CHAT_ID:
        logger.warning("DONO_CHAT_ID nao configurado - lead nao sera notificado")
        return

    emoji_class = {"QUENTE": "🔥", "MORNO": "☀️", "FRIO": "❄️"}
    emoji = emoji_class.get(lead["classificacao"], "📩")

    texto = f"{emoji} *NOVO LEAD - {lead['classificacao']}*\n"
    texto += f"_Score: {lead['score']} | Nicho: {lead['nicho']}_\n\n"

    for pergunta in BOT_CONFIG["perguntas"]:
        pid = pergunta["id"]
        if pid in lead["respostas"]:
            label = pergunta.get("label", pergunta["pergunta"].rstrip("?!."))
            texto += f"*{label}:* {lead['respostas'][pid]}\n"

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


async def finalizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Encerra a conversa: salva, notifica e agradece."""
    respostas = context.user_data["respostas"]
    score = calcular_score(respostas)

    lead = salvar_lead(respostas, score, update.effective_user)
    await notificar_dono(context, lead)

    nome = respostas.get("nome", "")
    telefone = respostas.get("telefone", "informado")
    msg_final = BOT_CONFIG["mensagem_final"].format(
        nome=nome,
        telefone=telefone,
        empresa=BOT_CONFIG["empresa"],
    )

    await update.message.reply_text(msg_final, reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


# ====================================================================
# COMANDOS EXTRAS
# ====================================================================
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ajuda."""
    await update.message.reply_text(
        "Comandos disponiveis:\n"
        "/start - Comecar (ou reiniciar) o atendimento\n"
        "/cancelar - Cancelar o atendimento atual\n"
        "/ajuda - Ver esta mensagem"
    )


# ====================================================================
# ENTRY POINT
# ====================================================================
def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN nao configurado. Copie .env.example para .env e preencha.")

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PERGUNTANDO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receber_resposta),
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

    logger.info(f"Bot iniciado | Nicho ativo: {BOT_CONFIG['nicho']}")
    logger.info(f"Empresa: {BOT_CONFIG['empresa']}")
    logger.info(f"Total de perguntas no fluxo: {len(BOT_CONFIG['perguntas'])}")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
