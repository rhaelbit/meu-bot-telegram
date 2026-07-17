"""
MOLDE PARA NOVO CLIENTE
=======================
Copie este arquivo para criar o perfil de um novo cliente.

Exemplo:
    cp clientes/_exemplo_novo_cliente.py clientes/imobiliaria_xyz.py

Depois, no .env, aponte:
    CLIENTE=imobiliaria_xyz
"""

CLIENTE = {
    # Nome do corretor/consultor que vai aparecer nas mensagens
    "nome_consultor": "Nome do Corretor",

    # Nome da imobiliaria/empresa do cliente
    "nome_imobiliaria": "Nome da Imobiliaria",

    # Produto/servico principal que a imobiliaria trabalha
    # Exemplos:
    # - "empreendimentos do programa Minha Casa Minha Vida"
    # - "imoveis de alto padrao"
    # - "imoveis para investimento e locacao"
    # - "casas e apartamentos usados"
    "produto_principal": "Descreva o produto principal aqui",

    # Regiao onde a imobiliaria atua
    "regiao_atuacao": "Cidade / Bairro / Estado",

    # Telefone/WhatsApp do consultor humano (para follow-up dos leads)
    "telefone_consultor": "XX XXXXX-XXXX",

    # Existe uma IA/atendente que atende ANTES e passa o lead?
    # Se sim, coloque o nome. Se nao, deixe None.
    "ia_anterior": None,

    # Frase de apresentacao no primeiro contato.
    # Se tem ia_anterior, mencione. Se nao, so se apresente normal.
    "apresentacao_inicial": (
        "Ola, tudo bem? Me chamo [Nome], sou consultor imobiliario da "
        "[Imobiliaria]. Como posso te ajudar?"
    ),
}
