"""
Perfil do CLIENTE: Israel / Direcional
======================================
Este e o SEU proprio perfil - o consultor original.
Use este arquivo como referencia para criar perfis de outros clientes.
"""

CLIENTE = {
    # Nome do consultor (aparece nas mensagens e apresentacao)
    "nome_consultor": "Israel",

    # Nome da imobiliaria / empresa
    "nome_imobiliaria": "Direcional",

    # Produto/nicho principal (Minha Casa Minha Vida, alto padrao, etc)
    "produto_principal": "empreendimentos do programa Minha Casa Minha Vida",

    # Regiao de atuacao
    "regiao_atuacao": "Nova Iguacu e regiao metropolitana do RJ",

    # Contato do consultor (aparece na notificacao para o dono)
    "telefone_consultor": "21 96407-5436",

    # IA anterior no fluxo (opcional - se cliente ja tem outra IA
    # que atende antes e passa o lead pra ele). Deixe None se nao houver.
    "ia_anterior": "Diana",

    # Como o consultor se apresenta na primeira interacao
    "apresentacao_inicial": (
        "Ola, tudo bem? Me chamo Israel, sou consultor imobiliario da "
        "Direcional. A Diana me encaminhou seu atendimento para dar "
        "continuidade e ajudar voce a encontrar a melhor opcao. "
        "Como posso te ajudar?"
    ),
}
