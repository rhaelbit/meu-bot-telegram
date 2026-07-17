"""
Configuracao: ADVOGADO
======================
Qualifica leads que buscam servicos juridicos.
"""

BOT_CONFIG = {
    "nicho": "advogado",
    "empresa": "Seu Escritorio de Advocacia",

    "mensagem_boas_vindas": (
        "Ola! Sou o assistente virtual do {empresa}.\n\n"
        "Para te atender melhor, vou fazer algumas perguntas rapidas sobre "
        "o seu caso. Todas as informacoes sao sigilosas.\n\n"
        "Se preferir cancelar, digite /cancelar."
    ),

    "mensagem_final": (
        "Recebemos suas informacoes, {nome}. ⚖️\n\n"
        "Um advogado especializado vai entrar em contato pelo telefone "
        "{telefone} para agendar uma consulta.\n\n"
        "Atenciosamente, {empresa}."
    ),

    "perguntas": [
        {
            "id": "area",
            "label": "Area do direito",
            "pergunta": "Qual a area do seu caso?",
            "opcoes": [
                "Trabalhista",
                "Civel",
                "Familia (divorcio, pensao, guarda)",
                "Previdenciario (INSS)",
                "Consumidor",
                "Criminal",
                "Empresarial / tributario",
                "Nao sei ao certo",
            ],
        },
        {
            "id": "urgencia",
            "label": "Urgencia",
            "pergunta": "Qual a urgencia da sua situacao?",
            "opcoes": [
                "Muito urgente (dias)",
                "Urgente (poucas semanas)",
                "Posso aguardar 1-2 meses",
                "Apenas pesquisando",
            ],
        },
        {
            "id": "situacao",
            "label": "Situacao atual",
            "pergunta": "Voce ja possui algum processo em andamento?",
            "opcoes": ["Sim", "Nao", "Nao tenho certeza"],
        },
        {
            "id": "descricao",
            "label": "Resumo do caso",
            "pergunta": "Descreva brevemente sua situacao (em poucas linhas):",
            "opcoes": None,
        },
        {
            "id": "cidade",
            "label": "Cidade",
            "pergunta": "Qual sua cidade?",
            "opcoes": None,
        },
        {
            "id": "nome",
            "label": "Nome",
            "pergunta": "Qual seu nome completo?",
            "opcoes": None,
        },
        {
            "id": "telefone",
            "label": "Telefone/WhatsApp",
            "pergunta": "Qual seu telefone com DDD?",
            "opcoes": None,
        },
    ],

    "scoring": {
        "urgencia": {
            "Muito urgente (dias)": 10,
            "Urgente (poucas semanas)": 7,
            "Posso aguardar 1-2 meses": 3,
            "Apenas pesquisando": 1,
        },
        "situacao": {"Sim": 6, "Nao": 4, "Nao tenho certeza": 3},
    },
}
