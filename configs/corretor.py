"""
Configuracao: CORRETOR DE IMOVEIS
=================================
Qualifica leads interessados em comprar/alugar imoveis.
"""

BOT_CONFIG = {
    "nicho": "corretor de imoveis",
    "empresa": "Sua Imobiliaria",

    "mensagem_boas_vindas": (
        "Ola! 👋 Sou o assistente virtual da {empresa}.\n\n"
        "Vou te fazer 6 perguntas rapidas para entender o que voce procura "
        "e conectar com o corretor ideal. Leva menos de 2 minutos!\n\n"
        "Se quiser cancelar a qualquer momento, e so digitar /cancelar."
    ),

    "mensagem_final": (
        "Perfeito, {nome}! ✅\n\n"
        "Recebemos suas informacoes e um corretor especializado vai entrar "
        "em contato pelo WhatsApp {telefone} em breve.\n\n"
        "Obrigado pelo interesse na {empresa}!"
    ),

    "perguntas": [
        {
            "id": "objetivo",
            "label": "Objetivo",
            "pergunta": "Voce quer comprar, alugar ou vender um imovel?",
            "opcoes": ["Comprar", "Alugar", "Vender"],
        },
        {
            "id": "tipo",
            "label": "Tipo de imovel",
            "pergunta": "Que tipo de imovel?",
            "opcoes": ["Apartamento", "Casa", "Terreno", "Comercial"],
        },
        {
            "id": "regiao",
            "label": "Regiao/Bairro",
            "pergunta": "Qual regiao ou bairro te interessa?",
            "opcoes": None,
        },
        {
            "id": "orcamento",
            "label": "Orcamento",
            "pergunta": "Qual sua faixa de orcamento?",
            "opcoes": [
                "Ate R$ 300 mil",
                "R$ 300k a R$ 500k",
                "R$ 500k a R$ 1 milhao",
                "Acima de R$ 1 milhao",
            ],
        },
        {
            "id": "prazo",
            "label": "Prazo para fechar",
            "pergunta": "Quando pretende fechar negocio?",
            "opcoes": ["Imediato", "1 a 3 meses", "3 a 6 meses", "Sem pressa"],
        },
        {
            "id": "pagamento",
            "label": "Forma de pagamento",
            "pergunta": "Como pretende pagar?",
            "opcoes": ["A vista", "Financiamento", "FGTS + financiamento"],
        },
        {
            "id": "nome",
            "label": "Nome",
            "pergunta": "Otimo! Qual seu nome completo?",
            "opcoes": None,
        },
        {
            "id": "telefone",
            "label": "WhatsApp",
            "pergunta": "E seu WhatsApp com DDD?",
            "opcoes": None,
        },
    ],

    # Pontuacao para classificar o lead (QUENTE / MORNO / FRIO)
    "scoring": {
        "objetivo": {"Comprar": 5, "Alugar": 3, "Vender": 4},
        "prazo": {
            "Imediato": 10,
            "1 a 3 meses": 7,
            "3 a 6 meses": 3,
            "Sem pressa": 1,
        },
        "pagamento": {
            "A vista": 10,
            "Financiamento": 5,
            "FGTS + financiamento": 4,
        },
    },
}
