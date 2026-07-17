"""
Configuracao: CLINICA DE ESTETICA
=================================
Qualifica leads interessados em procedimentos esteticos.
"""

BOT_CONFIG = {
    "nicho": "clinica de estetica",
    "empresa": "Sua Clinica",

    "mensagem_boas_vindas": (
        "Oi, tudo bem? ✨ Sou a assistente virtual da {empresa}.\n\n"
        "Vou te ajudar a encontrar o procedimento ideal e agendar uma "
        "avaliacao gratuita. Leva 1 minutinho!\n\n"
        "Se quiser cancelar, e so digitar /cancelar."
    ),

    "mensagem_final": (
        "Prontinho, {nome}! 💖\n\n"
        "Nossa equipe vai entrar em contato pelo WhatsApp {telefone} "
        "para agendar sua avaliacao gratuita.\n\n"
        "Ate breve na {empresa}!"
    ),

    "perguntas": [
        {
            "id": "procedimento",
            "label": "Procedimento de interesse",
            "pergunta": "Qual procedimento te interessa?",
            "opcoes": [
                "Botox / Preenchimento",
                "Harmonizacao facial",
                "Limpeza de pele",
                "Depilacao a laser",
                "Emagrecimento / gordura localizada",
                "Nao sei ainda",
            ],
        },
        {
            "id": "urgencia",
            "label": "Urgencia",
            "pergunta": "Quando gostaria de comecar?",
            "opcoes": [
                "Essa semana",
                "Nas proximas 2 semanas",
                "Neste mes",
                "Ainda estou pesquisando",
            ],
        },
        {
            "id": "ja_fez",
            "label": "Ja fez antes",
            "pergunta": "Voce ja fez algum procedimento estetico?",
            "opcoes": ["Sim, varios", "Sim, um ou dois", "Nunca fiz"],
        },
        {
            "id": "orcamento",
            "label": "Orcamento",
            "pergunta": "Qual investimento voce esta considerando?",
            "opcoes": [
                "Ate R$ 500",
                "R$ 500 a R$ 1.500",
                "R$ 1.500 a R$ 3.000",
                "Acima de R$ 3.000",
                "Prefiro conversar depois",
            ],
        },
        {
            "id": "nome",
            "label": "Nome",
            "pergunta": "Otimo! Qual seu nome?",
            "opcoes": None,
        },
        {
            "id": "telefone",
            "label": "WhatsApp",
            "pergunta": "E seu WhatsApp com DDD?",
            "opcoes": None,
        },
    ],

    "scoring": {
        "urgencia": {
            "Essa semana": 10,
            "Nas proximas 2 semanas": 7,
            "Neste mes": 4,
            "Ainda estou pesquisando": 1,
        },
        "orcamento": {
            "Ate R$ 500": 3,
            "R$ 500 a R$ 1.500": 5,
            "R$ 1.500 a R$ 3.000": 8,
            "Acima de R$ 3.000": 10,
            "Prefiro conversar depois": 2,
        },
    },
}
