"""
Configuracao: PERSONAL TRAINER
==============================
Qualifica leads interessados em acompanhamento fisico.
"""

BOT_CONFIG = {
    "nicho": "personal trainer",
    "empresa": "Seu Personal",

    "mensagem_boas_vindas": (
        "Fala, atleta! 💪 Sou o assistente virtual do {empresa}.\n\n"
        "Vou te fazer 5 perguntas rapidas para montar o plano de treino "
        "ideal para o seu perfil. Leva 1 minutinho!\n\n"
        "Digite /cancelar para sair a qualquer momento."
    ),

    "mensagem_final": (
        "Show, {nome}! 🔥\n\n"
        "Vou analisar seu perfil e te chamar no WhatsApp {telefone} com "
        "uma proposta personalizada de treino.\n\n"
        "Bora treinar!"
    ),

    "perguntas": [
        {
            "id": "objetivo",
            "label": "Objetivo",
            "pergunta": "Qual seu principal objetivo?",
            "opcoes": [
                "Emagrecer",
                "Ganhar massa muscular",
                "Melhorar condicionamento",
                "Reabilitacao / dor",
                "Performance esportiva",
            ],
        },
        {
            "id": "experiencia",
            "label": "Experiencia",
            "pergunta": "Qual seu nivel de experiencia com treino?",
            "opcoes": [
                "Nunca treinei",
                "Ja treinei mas parei",
                "Treino ha menos de 1 ano",
                "Treino ha mais de 1 ano",
            ],
        },
        {
            "id": "modalidade",
            "label": "Modalidade",
            "pergunta": "Onde prefere treinar?",
            "opcoes": [
                "Academia",
                "Em casa",
                "Ao ar livre",
                "Online / a distancia",
            ],
        },
        {
            "id": "frequencia",
            "label": "Frequencia semanal",
            "pergunta": "Quantas vezes por semana pode treinar?",
            "opcoes": ["2x", "3x", "4x", "5x ou mais"],
        },
        {
            "id": "investimento",
            "label": "Investimento mensal",
            "pergunta": "Qual investimento mensal considera?",
            "opcoes": [
                "Ate R$ 200",
                "R$ 200 a R$ 500",
                "R$ 500 a R$ 1.000",
                "Acima de R$ 1.000",
            ],
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
            "pergunta": "Seu WhatsApp com DDD?",
            "opcoes": None,
        },
    ],

    "scoring": {
        "experiencia": {
            "Nunca treinei": 8,
            "Ja treinei mas parei": 10,
            "Treino ha menos de 1 ano": 6,
            "Treino ha mais de 1 ano": 5,
        },
        "investimento": {
            "Ate R$ 200": 2,
            "R$ 200 a R$ 500": 6,
            "R$ 500 a R$ 1.000": 9,
            "Acima de R$ 1.000": 10,
        },
    },
}
