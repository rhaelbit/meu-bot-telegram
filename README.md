# Bot Qualificador de Leads no Telegram

Bot para captar e qualificar leads via Telegram com **dois modos** de operação:

- 🟢 **Modo Fixo** — fluxo de perguntas pré-definidas (rápido, sem custo, sem IA)
- 🔥 **Modo IA** — conversa natural com LLM (Groq) usando o cérebro do consultor

Um único código, N nichos, N clientes.

---

## O que o bot faz

1. Cliente entra no bot pelo Telegram e digita `/start`
2. **Modo Fixo:** faz perguntas em sequência com botões de resposta
3. **Modo IA:** conversa livremente como um consultor real, aplicando técnicas de venda
4. Salva o lead em JSON e notifica o dono no Telegram, com **score** e classificação:
   - 🔥 **QUENTE** (score ≥ 15) — pronto pra fechar
   - ☀️ **MORNO** (score 8-14) — precisa nutrir
   - ❄️ **FRIO** (score < 8) — apenas curioso

---

## Nichos disponíveis

### Modo Fixo (rápido, sem IA)
| Nicho | Arquivo | Uso típico |
|---|---|---|
| Corretor de imóveis | `configs/corretor.py` | Qualificação de comprador/locatário |
| Clínica de estética | `configs/clinica_estetica.py` | Agendamento de avaliação |
| Advogado | `configs/advogado.py` | Triagem de caso jurídico |
| Personal trainer | `configs/personal_trainer.py` | Captação de aluno |
| Dentista | `configs/dentista.py` | Agendamento odontológico |

### Modo IA (conversa natural)
| Nicho | Arquivo | Descrição |
|---|---|---|
| Corretor com IA | `configs/corretor_ia.py` | Consultor imobiliário completo com SPIN/BANT |

---

## Instalação rápida

### 1. Dependências
```bash
pip install -r requirements.txt
```

### 2. Criar bot no Telegram
Fale com `@BotFather` no Telegram → `/newbot` → guarde o token.

### 3. Descobrir seu Chat ID
Fale com `@userinfobot` no Telegram → ele te dá seu ID.

### 4. (Só pro modo IA) Criar conta grátis no Groq
Vá em [console.groq.com](https://console.groq.com), cadastre-se, e crie uma API Key no menu "API Keys". Começa com `gsk_...`.

### 5. Configurar `.env`
```bash
cp .env.example .env
```

Edite o `.env` preenchendo:

**Para Modo Fixo:**
```
BOT_TOKEN=seu_token_aqui
DONO_CHAT_ID=seu_chat_id_aqui
NICHO=corretor
```

**Para Modo IA:**
```
BOT_TOKEN=seu_token_aqui
DONO_CHAT_ID=seu_chat_id_aqui
NICHO=corretor_ia
GROQ_API_KEY=gsk_sua_chave_aqui
CLIENTE=direcional_israel
```

### 6. Rodar
```bash
python bot.py
```

Envie `/start` no seu bot pelo Telegram.

---

## Como adicionar um NOVO CLIENTE (Modo IA)

Cada cliente (imobiliária, consultório, etc) tem um "perfil" em `clientes/`.

### 1. Copiar o molde:
```bash
cp clientes/_exemplo_novo_cliente.py clientes/imobiliaria_xyz.py
```

### 2. Editar `clientes/imobiliaria_xyz.py`:
```python
CLIENTE = {
    "nome_consultor": "Maria Silva",
    "nome_imobiliaria": "Imobiliária XYZ",
    "produto_principal": "imóveis de alto padrão",
    "regiao_atuacao": "Barra da Tijuca, RJ",
    "telefone_consultor": "21 99999-1234",
    "ia_anterior": None,
    "apresentacao_inicial": "Olá! Sou a Maria, consultora da Imobiliária XYZ...",
}
```

### 3. Ativar no `.env`:
```
CLIENTE=imobiliaria_xyz
```

### 4. Reiniciar o bot.

**Não precisa mexer no `bot.py` nem no prompt da IA.** O mesmo cérebro se adapta ao novo cliente.

---

## Como funciona o Modo IA por dentro

```
Lead manda mensagem
        ↓
Bot envia pro LLM (Groq)
        ↓
LLM responde como o consultor
        ↓
Cada 2 turnos: extrai dados estruturados
        ↓
Quando tiver: objetivo + região + tipo + renda + nome + telefone
        ↓
Salva lead + notifica dono
```

Custo por lead: ~R$ 0,01 no Groq (na verdade, ainda é grátis dentro do tier free).

---

## Estrutura de arquivos

```
📁 meu-bot-telegram/
├── bot.py                      ← Motor universal (não mexer)
├── ai_engine.py                ← Motor do LLM (só usado no modo IA)
├── requirements.txt
├── .env                        ← Suas configs (não subir pro Git!)
├── .env.example
├── configs/
│   ├── corretor.py             ← Modo fixo
│   ├── clinica_estetica.py     ← Modo fixo
│   ├── advogado.py             ← Modo fixo
│   ├── dentista.py             ← Modo fixo
│   ├── personal_trainer.py     ← Modo fixo
│   └── corretor_ia.py          ← Modo IA (cérebro do consultor)
├── clientes/                   ← Perfis dos clientes (apenas modo IA)
│   ├── direcional_israel.py
│   └── _exemplo_novo_cliente.py
└── leads/                      ← Onde os leads são salvos (JSON)
```

---

## Onde ficam os leads salvos

Cada lead vira um arquivo JSON dentro de `leads/`:

```json
{
  "timestamp": "2026-07-17T14:32:10",
  "telegram_username": "joaocorretor",
  "nicho": "corretor de imoveis",
  "modo": "ia",
  "cliente": "Direcional",
  "score": 22,
  "classificacao": "QUENTE",
  "dados": {
    "objetivo": "moradia",
    "regiao": "Nova Iguacu",
    "tipo_imovel": "apartamento 2 quartos",
    "renda": "R$ 3500",
    "tipo_renda": "clt",
    "fgts": "sim",
    "nome": "Maria Silva",
    "telefone": "21 98888-7777"
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

---

## Solução de problemas

**"BOT_TOKEN nao configurado"** → Não criou/preencheu o `.env`.

**"Configuracao 'configs/xxx.py' nao encontrada"** → Variável `NICHO` no `.env` não corresponde a nenhum arquivo em `configs/`.

**"GROQ_API_KEY nao configurada"** → Você está usando modo IA mas não colocou a chave. Pegue em [console.groq.com](https://console.groq.com).

**"Perfil de cliente 'clientes/xxx.py' nao encontrado"** → Variável `CLIENTE` aponta pra arquivo que não existe. Verifique `clientes/`.

**Bot no Telegram não responde** → Confirme que `python bot.py` está rodando e mostrando `Bot iniciado`. Envie `/start` no chat.

**Dono não recebe notificação** → O dono precisa enviar `/start` no bot pelo menos 1 vez antes. Telegram bloqueia envios pra quem nunca falou com o bot.

**IA responde estranho ou em inglês** → Verifique se o system prompt do `configs/corretor_ia.py` está intacto (não editar sem cuidado).

---

## Licença

Código-fonte para uso próprio ou de clientes. Você pode:
- ✅ Adaptar para qualquer nicho e cliente
- ✅ Usar em projetos comerciais
- ✅ Cobrar pela implantação em clientes finais

Não é permitido:
- ❌ Revender o código-fonte como se fosse seu
- ❌ Redistribuir gratuitamente em canais públicos
