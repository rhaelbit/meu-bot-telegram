# 📋 PROSPECT — Beartoshi

> **Status atual:** 🟡 Em qualificação (aguardando reunião de descoberta)
>
> **Origem do lead:** Grupo Telegram de Trading (comentário orgânico sobre automação de reativação)
>
> **Data primeiro contato:** 30/07/2026
>
> **Última atualização:** 30/07/2026

---

## 👤 Identificação

| Campo | Valor |
|---|---|
| Nome/Apelido | Beartoshi 🥬🐻📈 |
| Canal de contato | Grupo Telegram de Trading |
| Cidade/Estado | (a descobrir) |
| Empresa/Negócio | (a descobrir — provavelmente varejo, dado o uso do Microvix) |
| Cargo | Provavelmente dono / sócio (tem autonomia de decisão técnica) |

---

## 🏢 Contexto do negócio

### Stack técnica já em uso:
- ✅ **ERP:** Microvix (varejo — moda, calçados, cosméticos ou suplementação)
- ✅ **CRM próprio** em desenvolvimento (já robusto, faltam telas)
- ✅ **Hardware:** Mac mini adquirido recentemente, ainda sem uso
- 🔎 Sistema tem API oficial documentada (Microvix)

### Nível de maturidade digital:
- **Alta** — codifica ou tem alguém que codifica
- Vocabulário sofisticado (usa termos como **LTV, análise preditiva, segmentação**)
- Já pesquisou o mercado de "vendedores IA" — **insatisfeito** com o que viu
- Compra ferramentas caras (Microvix + Mac mini)

---

## 🎯 Dores identificadas (na fala dele)

### 🔥 Dor principal — Ativação de base de clientes
Segmentos já identificados por ele:
1. **Clientes que não compram** (churned / inativos há X dias)
2. **Clientes que compraram apenas 1 vez** (single purchase)
3. **Clientes que só compram com desconto** (price-sensitive)
4. **Clientes que compram sem desconto** (premium / leais)
5. **Clientes novos** — precisa manter e aumentar LTV

### 🔥 Dor secundária — Automação de conteúdo
- Carrossel automatizado
- Vídeo UGC (User Generated Content)
- ⚠️ **Escopo separado** — atacar depois da Fase 1

### 💭 Contexto emocional (sinal-chave)
> *"Comprei um mac mini, chegou mas nem mexi ainda"*

**Interpretação:** ele está **sobrecarregado**. Tem grana, tem intenção, tem hardware — mas não tem tempo. **Este é o momento perfeito pra terceirizar** para alguém especializado.

---

## 💬 Histórico de conversas

### 📅 30/07/2026 — Post inicial no grupo (dele)

> "Será que consigo automatizar CRM, análise preditiva, vendas? Um agente entrar no meu ERP, analisar clientes que não compram marca X, produto X, por CEP há mais de XX dias, entrar em contato por WhatsApp pra fazer reativação de cliente, follow up, se no 3º ou 4º contato cliente não responder, mandar um cupom de desconto, quebrar objeções, responder como um nutricionista vendedor, fazer cross-sell, etc?"

**Nota:** Ele mencionou "nutricionista vendedor" — pode indicar que o negócio dele é do ramo de **nutrição / suplementação** (ou está apenas usando como exemplo genérico).

---

### 📅 30/07/2026 — Minha resposta (Israel)

Comentei no grupo posicionando conhecimento técnico, mencionando que já tinha construído algo parecido para outro nicho (imobiliário), e convidei pra conversa privada.

---

### 📅 30/07/2026 19:28 — Ele respondeu no privado (informações críticas)

1. **"Meu sistema é o ERP Microvix, tem API"**
2. **"Tudo que eu vi de vendedor IA, nada me animou"**
3. **"Eu preciso também criar automação pra conteúdo, carrossel principalmente e se der vídeo UGC"**
4. **"Você fez pra que nicho?"**

---

### 📅 30/07/2026 22:06 — Continuação da conversa

1. **"vc é programador?"**
2. **"comecei fazer um CRM, tá bem robusto, mas preciso melhorar as telas ainda"**
3. **"análise preditiva, etc"**
4. **"tem muito cliente na base que não compra, cliente que só comprou uma vez, cliente que compra com desconto, sem desconto etc"**
5. **"preciso ativar esses clientes"**
6. **"e cliente novo também, manter LTV"**
7. **"preciso fazer muita coisa, até comprei um mac mini, chegou mas nem mexi ainda"**

---

### 📅 30/07/2026 — Minha resposta (Israel)

Respondi:
- Que não sou programador tradicional, mas **especialista em automação comercial com IA**
- Elogiei o fato dele já ter CRM próprio (simplifica minha entrega)
- Traduzi os 4 segmentos dele em jornadas específicas do bot
- Enfatizei: "tirar dor do teu prato" (não dar mais trabalho)
- Convidei pra reunião de 30 min com 5 perguntas de descoberta

**Aguardando resposta.**

---

## 🎯 Estratégia de abordagem

### Posicionamento comigo:
Eu **NÃO** sou:
- Programador tradicional (front/back/banco)
- Concorrente do CRM dele
- Vendedor de solução genérica

Eu **SOU**:
- Especialista em automação comercial com IA
- Ponte entre o CRM dele e o cliente final (via WhatsApp)
- Alguém que **tira dor do prato** dele

### Ângulo de venda:
- Não vender "mais um projeto pra ele fazer"
- Vender **"tira isso do teu prato"** enquanto ele foca no negócio
- Aproveitar o CRM que ele já tem (não substituir)
- Cérebro (IA) + Canal (WhatsApp) — infraestrutura fica com ele

---

## 💰 Ticket projetado

Baseado nos sinais coletados (Microvix + Mac mini + CRM próprio + vocabulário sênior):

### 📦 Fase 1 — MVP Reativação (sem integração CRM ainda)
- **Setup:** R$ 4.997 (à vista) ou 6x R$ 899
- **Recorrente:** R$ 397/mês
- **Prazo:** 20-25 dias
- **Escopo:**
  - Bot IA com persona de vendedor consultor
  - Recebe lista de clientes segmentados (CSV/Excel exportado do CRM dele)
  - Jornadas diferentes por segmento (4 tipos)
  - Sequência de reativação (3-5 contatos, cupom no 3º)
  - Deploy 24h + WhatsApp via Evolution API

### 📦 Fase 2 — Integração CRM/Microvix
- **Setup adicional:** R$ 5.997
- **Recorrente:** +R$ 397/mês (total R$ 794/mês)
- **Prazo:** 25-30 dias
- **Escopo:**
  - Conecta direto ao CRM dele (API)
  - Consulta Microvix para dados de compra
  - Segmentação automática (sem CSV)
  - Atualização de status no CRM

### 📦 Fase 3 — Analítica Preditiva
- **Setup adicional:** R$ 5.997
- **Recorrente:** +R$ 397/mês (total R$ 1.191/mês)
- **Prazo:** 30-45 dias
- **Escopo:**
  - Score de churn (probabilidade de perda)
  - Score de conversão
  - Dashboard com métricas
  - Recomendação de próxima ação

### 📦 Módulo Separado — Automação de Conteúdo
- **Setup:** R$ 2.997-4.997
- **Recorrente:** R$ 197-397/mês
- **Escopo:** carrossel automatizado, roteiros de UGC (produto separado, tratar após Fase 1)

---

### 💎 Totais projetados

| Cenário | Setup | Recorrente | 12 meses |
|---|---|---|---|
| **Só Fase 1** | R$ 4.997 | R$ 4.764 | **R$ 9.761** |
| **Fases 1+2** | R$ 10.994 | R$ 9.528 | **R$ 20.522** |
| **Projeto completo (F1+F2+F3)** | R$ 16.991 | R$ 14.292 | **R$ 31.283** |
| **Completo + Conteúdo** | R$ 21.988 | R$ 18.660 | **R$ 40.648** |

---

## 📋 Perguntas de descoberta (pra reunião)

Quando ele topar a reunião, fazer nessa ordem (uma por vez, esperando resposta):

### 🔍 Bloco 1 — Contexto do negócio
1. Qual o segmento/nicho da tua empresa? (moda? suplementação? cosméticos?)
2. Quanto tempo de mercado?
3. Faturamento aproximado mensal? (opcional — pode ser sensível)

### 🔍 Bloco 2 — Base e volume
4. Quantos **clientes ativos** você tem na base? (últimos 12 meses)
5. Quantos **clientes inativos** (não compram há 90+ dias)?
6. Ticket médio de venda?
7. Qual sua taxa de recompra atual?

### 🔍 Bloco 3 — Operação atual
8. Hoje quem faz reativação — ninguém, atendente humano, automação simples?
9. Já usa WhatsApp Business API oficial (Meta) ou WhatsApp Web?
10. Já testou algum bot/automação antes? Por que não deu certo?

### 🔍 Bloco 4 — Expectativas
11. Qual seria uma "vitória" no primeiro mês pra você? (número real)
12. Prazo ideal pra ter isso funcionando?
13. Prefere entregar rápido (piloto simples) ou completo (integrado)?

---

## 🛡️ Argumentos para objeções esperadas

### ❓ "Meu primo/sobrinho faz isso mais barato"
**Resposta:**
> "Bot com IA é fácil de fazer feio. Difícil é fazer que **converte**. Meu bot aplica SPIN Selling e BANT — metodologia real de vendas. Isso vale a diferença entre 10% e 40% de conversão."

### ❓ "Já tentei automação, não funciona"
**Resposta:**
> "A maioria das automações são fluxos rígidos com botão. Isso realmente não funciona pra reativação — cliente inativo precisa de **conversa humana**, não menu. Meu bot conversa com LLM (IA generativa) — soa humano, adapta a cada cliente."

### ❓ "Prefiro contratar programador full-time por esse valor"
**Resposta:**
> "Contratar programador seria R$ 5-8k/mês + encargos + tempo pra ensinar sobre IA + treinamento em vendas. Comigo você paga só pelo resultado, sem CLT, sem treinamento, e já vem com metodologia pronta."

### ❓ "Não sei se vou usar direito"
**Resposta:**
> "Justamente por isso incluo **1 semana de acompanhamento pós-implantação** — chamadas semanais pra ver os primeiros leads chegando. Se em 30 dias não recuperou o custo, garanto devolução."

### ❓ "É muito caro"
**Resposta (baseada em ROI):**
> "Vamos pensar assim: um vendedor humano faz uns 40-50 contatos qualificados por dia. Meu bot faz 500-1000 (na base que ele tem). Se cada contato tem 5% de conversão em recompra, e teu ticket médio é [X], em 30 dias ele traz [Y]. O bot se paga em 15-30 dias."

---

## 📅 Timeline / Próximos passos

- [x] **30/07/2026** — Primeiro contato no grupo
- [x] **30/07/2026** — Ele iniciou conversa privada (super sinal)
- [x] **30/07/2026** — Respondi com posicionamento estratégico
- [ ] **Aguardando** — resposta dele sobre reunião
- [ ] **Se topar reunião:**
  - [ ] Gravar vídeo demo do bot (antes da reunião)
  - [ ] Estudar Microvix API (docs oficiais)
  - [ ] Preparar Google Meet ou WhatsApp Call
  - [ ] Ir na reunião com as 13 perguntas de descoberta
  - [ ] Levar Postman aberto (pra dar hello world na API ao vivo, se topar)
- [ ] **Pós-reunião:**
  - [ ] Enviar proposta escrita em até 48h
  - [ ] Follow-up após 3 dias se não responder
  - [ ] Follow-up após 7 dias se não responder

---

## 🚨 Cuidados especiais com este cliente

### ⚠️ Ele é técnico
Não subestimar. Vai perceber gambiarra. **Fala com propriedade.**

### ⚠️ Já se decepcionou com IA vendedora
"Nada me animou". **Não vender como todo mundo.** Diferenciar pela metodologia + personalização real.

### ⚠️ Vai querer entender o "como"
Programadores gostam de entender arquitetura. **Deixa preparada uma explicação de 5 min** sobre stack: Python + Groq (Llama 3.3) + Evolution API + Deploy Railway + JSON mode pra extração.

### ⚠️ Cuidado com preço
Não precifica sem descoberta. Ele é técnico o suficiente pra achar valor "chutado" no ar. **Sempre precifica baseado em escopo definido.**

### ⚠️ Ele pode querer "só a IA / cérebro"
Se ele quiser só o motor (ele integra sozinho), o preço muda:
- **"White label" motor da IA:** R$ 3.997 setup + R$ 197/mês (usa a API dele mesmo)
- Nesse caso, ele assume responsabilidade da integração

---

## 💡 Argumentos exclusivos deste cliente

### 🎯 Frase de ancoragem (usar na reunião)
> "Você tá construindo o CRM. Isso é o **corpo**. Eu construo o **cérebro** que faz esse corpo agir na hora certa com cada cliente. Junto, vira máquina de reativação."

### 🎯 Comparação forte
> "Programador comum construiria um sistema. Eu construo um **vendedor virtual** que aplica método de vendas real."

### 🎯 Chamada de valor
> "Cada dia que essa base fica sem ser trabalhada é dinheiro deixado na mesa. Se 1% desses clientes inativos recomprar por mês, isso já paga meu serviço por 3 anos."

---

## 📝 Anotações livres

*(Espaço pra você adicionar observações à medida que a conversa evolui)*

- 
- 
- 

---

## 🔗 Links úteis para consulta

- [Microvix - Área de Desenvolvedor](https://microvix.com.br)
- [Documentação Evolution API](https://doc.evolution-api.com/)
- [Groq Console](https://console.groq.com)
- Meu bot atual (rodando): `@[seu bot]_bot`
- Repositório: [github.com/rhaelbit/meu-bot-telegram](https://github.com/rhaelbit/meu-bot-telegram)

---

*Documento vivo — atualizar após cada interação com o prospect.*

*Última atualização: 30/07/2026 por Israel Villaça*
