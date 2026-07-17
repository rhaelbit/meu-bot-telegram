"""
AI Engine - Motor de conversacao com LLM (Groq)
================================================
Responsavel por:
1. Conversar naturalmente com o lead (usando o cerebro/prompt do cliente)
2. Extrair dados estruturados da conversa periodicamente
3. Detectar quando ja coletou informacao suficiente para finalizar

Usa a API do Groq (grátis) com modelo Llama 3.3 70B.
"""

import os
import json
import logging
from groq import Groq

logger = logging.getLogger(__name__)

# Modelo padrao - Llama 3.3 no tier gratuito do Groq
MODELO_PADRAO = "llama-3.3-70b-versatile"
MODELO_EXTRACAO = "llama-3.1-8b-instant"  # Mais rapido/barato para extrair JSON


# --------------------------------------------------------------------
# CLIENT GROQ
# --------------------------------------------------------------------
_client = None


def obter_cliente_groq():
    """Retorna o client Groq (cria uma vez e reusa)."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise SystemExit(
                "GROQ_API_KEY nao configurada. "
                "Pegue sua chave gratuita em https://console.groq.com "
                "e adicione no arquivo .env"
            )
        _client = Groq(api_key=api_key)
    return _client


# --------------------------------------------------------------------
# CONVERSA COM O LEAD
# --------------------------------------------------------------------
def montar_system_prompt(template: str, cliente: dict) -> str:
    """
    Preenche os placeholders do template com dados do cliente.
    Ex: {nome_consultor} vira 'Israel', {nome_imobiliaria} vira 'Direcional'.
    """
    # Trata ia_anterior=None de forma elegante (remove a mencao se nao tiver)
    if cliente.get("ia_anterior") is None:
        cliente = {**cliente, "ia_anterior": "nossa equipe"}

    try:
        return template.format(**cliente)
    except KeyError as e:
        logger.error(f"Placeholder faltando no perfil do cliente: {e}")
        raise


def conversar_com_lead(historico: list, system_prompt: str) -> str:
    """
    Uma rodada de conversa. Recebe o historico e retorna a resposta da IA.

    Args:
        historico: lista de dicts [{"role": "user"|"assistant", "content": "..."}, ...]
        system_prompt: instrucoes completas do consultor

    Returns:
        Texto da resposta da IA
    """
    client = obter_cliente_groq()

    mensagens = [{"role": "system", "content": system_prompt}] + historico

    try:
        resposta = client.chat.completions.create(
            model=MODELO_PADRAO,
            messages=mensagens,
            temperature=0.7,
            max_tokens=500,
            top_p=0.9,
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Erro ao chamar LLM: {e}")
        return (
            "Desculpe, tive uma instabilidade agora. "
            "Voce pode repetir sua ultima mensagem, por favor?"
        )


# --------------------------------------------------------------------
# EXTRACAO ESTRUTURADA DE DADOS DO LEAD
# --------------------------------------------------------------------
def extrair_dados_do_lead(
    historico: list,
    campos: list,
    campos_atuais: dict = None,
) -> dict:
    """
    Le a conversa inteira e extrai os campos estruturados.
    Usa JSON mode para garantir formato valido.

    Args:
        historico: lista de mensagens da conversa
        campos: lista dos campos a extrair (ex: ["objetivo", "regiao", ...])
        campos_atuais: o que ja foi extraido antes (para preservar)

    Returns:
        Dict com os campos preenchidos (ou null quando ainda nao mencionado)
    """
    client = obter_cliente_groq()
    campos_atuais = campos_atuais or {}

    # Monta descricao dos campos
    campos_lista = "\n".join([f'  - "{c}"' for c in campos])

    # Serializa conversa
    conversa_texto = ""
    for msg in historico:
        papel = "Lead" if msg["role"] == "user" else "Consultor"
        conversa_texto += f"\n{papel}: {msg['content']}"

    prompt_extracao = f"""Voce e um extrator de dados. Sua tarefa e analisar a conversa abaixo entre um consultor imobiliario e um lead, e extrair informacoes especificas.

CAMPOS A EXTRAIR (retorne TODOS, mesmo os que ainda estao vazios):
{campos_lista}

REGRAS:
1. Se o lead ainda NAO forneceu a informacao, coloque null
2. Se forneceu parcialmente, capture o que foi dito
3. Normalize valores: use minusculas para strings simples ("moradia", "clt", "apartamento")
4. Para numeros (renda, valores), retorne como string incluindo a moeda
5. Para telefones, capture no formato: "DDD numero"
6. Nao invente. Se em duvida, use null

Dados ja extraidos anteriormente (preserve se ainda validos):
{json.dumps(campos_atuais, ensure_ascii=False)}

CONVERSA:
{conversa_texto}

Responda APENAS com o JSON, sem comentarios."""

    try:
        resposta = client.chat.completions.create(
            model=MODELO_EXTRACAO,
            messages=[{"role": "user", "content": prompt_extracao}],
            temperature=0.1,
            max_tokens=600,
            response_format={"type": "json_object"},
        )
        dados = json.loads(resposta.choices[0].message.content)

        # Mescla com o que ja tinha - preserva campos existentes se novo veio null
        resultado = dict(campos_atuais)
        for campo in campos:
            valor_novo = dados.get(campo)
            if valor_novo is not None and valor_novo != "null" and valor_novo != "":
                resultado[campo] = valor_novo
            elif campo not in resultado:
                resultado[campo] = None

        return resultado

    except json.JSONDecodeError as e:
        logger.error(f"JSON invalido do extrator: {e}")
        return campos_atuais
    except Exception as e:
        logger.error(f"Erro no extrator: {e}")
        return campos_atuais


# --------------------------------------------------------------------
# COMPLETUDE DO LEAD
# --------------------------------------------------------------------
def lead_esta_completo(dados: dict, campos_minimos: list) -> bool:
    """
    Verifica se ja coletou o minimo necessario para finalizar.

    Args:
        dados: dict com os campos extraidos ate agora
        campos_minimos: lista dos campos que precisam estar preenchidos

    Returns:
        True se todos os campos minimos tem valor
    """
    for campo in campos_minimos:
        valor = dados.get(campo)
        if not valor or valor in ("null", None, ""):
            return False
    return True


def contar_campos_preenchidos(dados: dict, campos: list) -> int:
    """Conta quantos campos ja tem valor (util para scoring)."""
    return sum(
        1
        for c in campos
        if dados.get(c) and dados.get(c) not in ("null", None, "")
    )
