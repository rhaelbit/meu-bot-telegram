# Bot Qualificador de Leads no Telegram

Bot pronto para captar e qualificar leads via Telegram, com fluxo de perguntas personalizado por nicho, pontuação automática (lead QUENTE/MORNO/FRIO) e notificação imediata para o dono do negócio.

**Um único código, N nichos diferentes** — basta trocar o arquivo de configuração.

---

## O que o bot faz

1. Cliente entra no bot pelo Telegram e digita `/start`
2. Bot faz uma sequência de perguntas (personalizada por nicho)
3. Salva a resposta em arquivo JSON local
4. Calcula um **score** com base nas respostas e classifica o lead:
   - 🔥 **QUENTE** — pronto pra fechar
   - ☀️ **MORNO** — precisa nutrir
   - ❄️ **FRIO** — apenas curioso
5. Envia o lead formatado direto no Telegram do dono do negócio

---

## Nichos já configurados

| Nicho | Arquivo | Uso típico |
|---|---|---|
| Corretor de imóveis | `configs/corretor.py` | Qualificação de comprador/locatário |
| Clínica de estética | `configs/clinica_estetica.py` | Agendamento de avaliação |
| Advogado | `configs/advogado.py` | Triagem de caso jurídico |
| Personal trainer | `configs/personal_trainer.py` | Captação de aluno |
| Dentista | `configs/dentista.py` | Agendamento odontológico |

---

## Instalação (passo a passo, sem enrolação)

### 1. Instalar Python
Você precisa do Python 3.10 ou superior. Se não tiver, baixe em [python.org](https://www.python.org/downloads/).

### 2. Instalar as dependências

Abra o terminal na pasta do projeto e rode:

```bash
pip install -r requirements.txt
```

### 3. Criar seu bot no Telegram

1. No Telegram, procure por `@BotFather`
2. Envie `/newbot`
3. Escolha um nome e um username (deve terminar em `bot`, ex: `imobiliariaXYZbot`)
4. Ele vai te dar um **TOKEN** (algo como `123456:ABC-DEF...`) — guarde

### 4. Descobrir seu Chat ID (pra receber os leads)

1. No Telegram, procure por `@userinfobot`
2. Envie qualquer mensagem
3. Ele te retorna seu **Chat ID** (um número, ex: `987654321`)

### 5. Configurar o `.env`

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Abra o `.env` e preencha:

```
BOT_TOKEN=123456:ABC-DEF-seu-token
DONO_CHAT_ID=987654321
NICHO=corretor
```

Onde `NICHO` é o nome do arquivo dentro de `configs/` (sem o `.py`).

### 6. Rodar o bot

```bash
python bot.py
```

Pronto. Envie `/start` para o seu bot no Telegram e teste.

---

## Como adaptar para um novo nicho

1. Copie um dos arquivos existentes: `cp configs/corretor.py configs/meu_nicho.py`
2. Abra `configs/meu_nicho.py` e edite:
   - `nicho` e `empresa`
   - `mensagem_boas_vindas` e `mensagem_final`
   - Lista de `perguntas` (id, texto, opções ou `None` para resposta livre)
   - `scoring` — quais respostas aumentam a pontuação do lead
3. No `.env`, mude para `NICHO=meu_nicho`
4. Reinicie o bot

**Não precisa mexer no `bot.py`.** Toda a personalização é feita no arquivo de config.

---

## Estrutura das perguntas

Cada pergunta é um dicionário com:

```python
{
    "id": "orcamento",              # identificador unico (sem espaco/acento)
    "label": "Orcamento",           # como aparece na notificacao ao dono
    "pergunta": "Qual seu orcamento?",  # texto que o cliente ve
    "opcoes": ["Ate 300k", "300k-500k"],  # None = resposta livre
}
```

## Como funciona o scoring

Cada resposta pode valer pontos. O total classifica o lead:
- **>= 15 pontos** → QUENTE (o dono deve ligar em minutos)
- **8 a 14 pontos** → MORNO (colocar em nutrição)
- **abaixo de 8** → FRIO (arquivar ou automatizar)

Exemplo no `configs/corretor.py`:

```python
"scoring": {
    "prazo": {
        "Imediato": 10,       # quem quer comprar agora vale 10 pontos
        "1 a 3 meses": 7,
        "Sem pressa": 1,
    },
    "pagamento": {
        "A vista": 10,
        "Financiamento": 5,
    },
},
```

---

## Onde ficam os leads salvos

Todo lead vira um arquivo JSON dentro da pasta `leads/`, com nome tipo:
`lead_20260717_143210_123456789.json`

Exemplo do conteúdo:

```json
{
  "timestamp": "2026-07-17T14:32:10",
  "telegram_username": "joaocorretor",
  "nicho": "corretor de imoveis",
  "score": 22,
  "classificacao": "QUENTE",
  "respostas": {
    "objetivo": "Comprar",
    "tipo": "Apartamento",
    "regiao": "Jardins - SP",
    "orcamento": "R$ 500k a R$ 1 milhao",
    "prazo": "Imediato",
    "pagamento": "A vista",
    "nome": "Maria Silva",
    "telefone": "11 98888-7777"
  }
}
```

---

## Deploy 24/7 (opcional)

O bot precisa estar rodando pra funcionar. Opções:

| Plataforma | Custo | Dificuldade |
|---|---|---|
| Seu computador ligado | Grátis | Fácil (mas precisa ficar ligado) |
| [Railway](https://railway.app) | ~$5/mês | Fácil (deploy via GitHub) |
| [Render](https://render.com) | Free tier | Média |
| VPS (Hetzner, DigitalOcean) | ~$5/mês | Difícil |

Recomendo Railway para começar.

---

## Solução de problemas

**"BOT_TOKEN nao configurado"**
→ Você não criou o arquivo `.env` ou não preencheu o token. Volte ao passo 5.

**"Configuracao 'configs/xxx.py' nao encontrada"**
→ A variável `NICHO` no `.env` não corresponde a nenhum arquivo. Verifique os nomes em `configs/`.

**Bot não responde no Telegram**
→ Verifique se o `python bot.py` está rodando e mostrando `Bot iniciado`. Se sim, envie `/start` (com barra) diretamente no chat do bot.

**Dono não recebe os leads**
→ O bot precisa "conhecer" o dono antes. O dono deve enviar `/start` pelo menos 1 vez no chat do bot, senão o Telegram bloqueia o envio.

---

## Licença de uso

Este bot é entregue como código-fonte completo para uso próprio ou de clientes. Você pode:
- ✅ Adaptar para qualquer nicho
- ✅ Usar em projetos comerciais próprios
- ✅ Instalar para clientes (serviço de implementação)

Não é permitido:
- ❌ Revender o código-fonte como se fosse seu
- ❌ Redistribuir gratuitamente em canais públicos
