"""
Configuracao: DENTISTA / CLINICA ODONTOLOGICA
=============================================
Qualifica leads interessados em tratamentos odontologicos.
"""

BOT_CONFIG = {
    "nicho": "dentista",
    "empresa": "Sua Clinica Odontologica",

    "mensagem_boas_vindas": (
        "Ola! 😁 Sou o assistente da {empresa}.\n\n"
        "Vou te ajudar a agendar sua consulta de forma rapida. Preciso "
        "apenas de algumas informacoes.\n\n"
        "Digite /cancelar se quiser sair."
    ),

    "mensagem_final": (
        "Perfeito, {nome}! ✨\n\n"
        "Nossa secretaria vai entrar em contato pelo WhatsApp {telefone} "
        "para agendar sua consulta.\n\n"
        "Ate breve na {empresa}!"
    ),

    "perguntas": [
        {
            "id": "tratamento",
            "label": "Tratamento",
            "pergunta": "Qual tratamento voce procura?",
            "opcoes": [
                "Limpeza / avaliacao",
                "Clareamento dental",
                "Aparelho / ortodontia",
                "Implante",
                "Lente / faceta",
                "Tratamento de canal / urgencia",
                "Nao sei ainda",
            ],
        },
        {
            "id": "urgencia",
            "label": "Urgencia",
            "pergunta": "Tem alguma urgencia (dor, quebrou dente, etc)?",
            "opcoes": [
                "Sim, com dor / urgencia",
                "Sem dor, mas quero rapido",
                "Sem pressa, quando der",
            ],
        },
        {
            "id": "ja_cliente",
            "label": "Ja e cliente",
            "pergunta": "Voce ja e cliente da clinica?",
            "opcoes": ["Sim, sou cliente", "Nao, primeira vez"],
        },
        {
            "id": "convenio",
            "label": "Convenio",
            "pergunta": "Usa convenio odontologico?",
            "opcoes": ["Sim", "Nao, particular", "Ainda nao sei"],
        },
        {
            "id": "nome",
            "label": "Nome",
            "pergunta": "Qual seu nome?",
            "opcoes": None,
        },
        {
            "id": "telefone",
            "label": "WhatsApp",
            "pergunta": "WhatsApp com DDD?",
            "opcoes": None,
        },
    ],

    "scoring": {
        "urgencia": {
            "Sim, com dor / urgencia": 10,
            "Sem dor, mas quero rapido": 6,
            "Sem pressa, quando der": 2,
        },
        "tratamento": {
            "Implante": 10,
            "Lente / faceta": 9,
            "Aparelho / ortodontia": 8,
            "Clareamento dental": 6,
            "Tratamento de canal / urgencia": 7,
            "Limpeza / avaliacao": 4,
            "Nao sei ainda": 3,
        },
    },
}
