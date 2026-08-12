# 🇧🇷 GUIA EM PORTUGUÊS — Data Engineering Zoomcamp

> **Curso gratuito de Engenharia de Dados** — do zero ao pipeline completo em produção.
> Criado por [DataTalks.Club](https://datatalks.club/) — traduzido e adaptado por Israel Villaça.

---

## 📺 Como assistir

1. **Vídeos:** [Playlist completa no YouTube](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
2. **Legendas PT-BR:** No vídeo → ⚙️ → Legendas → Traduzir automaticamente → Português
3. **Material escrito:** Neste repositório (pastas por módulo)
4. **Dúvidas:** [Slack DataTalks.Club](https://datatalks.club/slack.html) canal `#course-data-engineering`

---

## 🗺️ MAPA DO CURSO (7 Módulos + Workshops + Projeto Final)

| Módulo | Tema | Duração | Ferramentas |
|--------|------|---------|-------------|
| 1 | Docker + Terraform | 1-2 semanas | Docker, PostgreSQL, Terraform, GCP |
| 2 | Orquestração de Workflows | 1-2 semanas | Kestra |
| W1 | Workshop: Ingestão de Dados | 1 semana | dlt (data load tool) |
| 3 | Data Warehouse | 1-2 semanas | BigQuery, SQL avançado |
| 4 | Analytics Engineering | 1-2 semanas | dbt, DuckDB, BigQuery |
| 5 | Plataformas de Dados | 1-2 semanas | Bruin, pipelines end-to-end |
| 6 | Processamento em Lote | 1-2 semanas | Apache Spark, PySpark |
| 7 | Streaming | 1-2 semanas | Apache Kafka, KSQL |
| Final | Projeto Final | 2-3 semanas | Tudo junto |

**Tempo total estimado:** 9-12 semanas (2-3 meses no teu ritmo)

---

---

# 📦 MÓDULO 1: Docker + Terraform (Containerização e Infraestrutura como Código)

## O que tu vai aprender:
- ✅ Docker e Docker Compose (tu já sabe 80% disso!)
- ✅ Rodar PostgreSQL em container
- ✅ Ingerir dados com Python
- 🆕 Terraform (infraestrutura como código)
- 🆕 Google Cloud Platform (GCP) básico

## 📺 Vídeos (em ordem):

### Aula 1.1 — Introdução ao curso
- **Vídeo:** https://www.youtube.com/watch?v=JgspdlKXS-w
- **O que cobre:** Visão geral do curso, arquitetura, ferramentas
- **Duração:** ~15 min

### Aula 1.2 — Docker + PostgreSQL (Workshop prático)
- **Vídeo:** https://www.youtube.com/watch?v=lP8xXebHmuE
- **O que cobre:** Dockerfile, docker-compose, rodar PostgreSQL em container, ingerir dados
- **Material:** [01-docker-terraform/docker-sql/](01-docker-terraform/docker-sql/)
- **Duração:** ~40 min
- **💡 Tu já sabe isso!** Fizemos exatamente isso com o monitor WhatsApp

### Aula 1.3 — SQL Refresher
- **Vídeo:** https://www.youtube.com/watch?v=QEcps_iskgg
- **O que cobre:** JOINs, GROUP BY, ORDER BY, filtros — revisão de SQL
- **Material:** [01-docker-terraform/docker-sql/10-sql-refresher.md](01-docker-terraform/docker-sql/10-sql-refresher.md)
- **Duração:** ~30 min

### Aula 1.4 — Introdução ao GCP
- **Vídeo:** https://www.youtube.com/watch?v=18jIzE41fJ4
- **O que cobre:** O que é Google Cloud, serviços principais, como criar conta
- **Duração:** ~10 min
- **💡 GCP tem $300 de crédito grátis** — usa pra praticar

### Aula 1.5 — Terraform: Conceitos e Visão Geral
- **Vídeo:** https://www.youtube.com/watch?v=s2bOYDCKl_M
- **O que cobre:** O que é Terraform, por que usar, conceitos básicos
- **Material:** [01-docker-terraform/terraform/](01-docker-terraform/terraform/)
- **Duração:** ~15 min

### Aula 1.6 — Terraform: Deploy Básico
- **Vídeo:** https://www.youtube.com/watch?v=Y2ux7gq3Z0o
- **O que cobre:** Primeiro deploy com Terraform (1 arquivo)
- **Duração:** ~20 min

### Aula 1.7 — Terraform: Variáveis
- **Vídeo:** https://www.youtube.com/watch?v=PBi0hHjLftk
- **O que cobre:** Usar variáveis no Terraform, deploy com arquivo de variáveis
- **Duração:** ~15 min

### 📝 Homework (Exercício):
- [Exercício do Módulo 1](cohorts/2026/01-docker-terraform/homework.md)
- Faz DEPOIS de assistir todos os vídeos

---

## 🛠️ O que tu precisa instalar pro Módulo 1:

| Ferramenta | Tu já tem? | Como instalar |
|-----------|-----------|---------------|
| Docker | ✅ Já instalou hoje! | — |
| Python | ✅ Provavelmente já tem | `python --version` no terminal |
| Git | ✅ Instalou hoje! | — |
| Terraform | 🆕 Instalar | https://developer.hashicorp.com/terraform/install |
| Conta GCP | 🆕 Criar | https://cloud.google.com/free ($300 grátis) |

---

---

# 📦 MÓDULO 2: Orquestração de Workflows

## O que tu vai aprender:
- 🆕 O que é Data Lake vs Data Warehouse
- 🆕 Orquestração de pipelines (agendar, monitorar, reexecutar)
- 🆕 Kestra (ferramenta de orquestração)

## 📺 Vídeos:
- Material na pasta: [02-workflow-orchestration/](02-workflow-orchestration/)
- Vídeos na playlist do YouTube (procurar por "Module 2" ou "Workflow Orchestration")

## 💡 Conceito-chave:
> **Orquestração** = automatizar e agendar pipelines de dados. Ex: "Todo dia às 6h, puxa dados da API, transforma e salva no banco". É o Airflow/Kestra fazendo isso pra ti, sem tu precisar rodar manualmente.

---

---

# 📦 MÓDULO 3: Data Warehouse (BigQuery)

## O que tu vai aprender:
- 🆕 O que é Data Warehouse (vs banco relacional normal)
- 🆕 BigQuery (Data Warehouse do Google, grátis até 1TB/mês de queries)
- 🆕 Particionamento e Clustering (performance)
- 🆕 ML no BigQuery (Machine Learning direto no SQL!)

## 📺 Vídeos:
- Material na pasta: [03-data-warehouse/](03-data-warehouse/)

## 💡 Conceito-chave:
> **Data Warehouse** = banco de dados otimizado pra ANÁLISE (não pra transações). PostgreSQL é bom pra app. BigQuery é bom pra analisar milhões de linhas rápido.

---

---

# 📦 MÓDULO 4: Analytics Engineering (dbt)

## O que tu vai aprender:
- 🆕 O que é Analytics Engineering
- 🆕 dbt (data build tool) — transformação de dados com SQL
- 🆕 Modelagem de dados (star schema, dimensões, fatos)
- 🆕 Testes e documentação de dados

## 📺 Vídeos:
- Material na pasta: [04-analytics-engineering/](04-analytics-engineering/)

## 💡 Conceito-chave:
> **dbt** = tu escreve SQL de transformação e o dbt cuida de: ordem de execução, testes, documentação, versionamento. É o "git pra dados".

## 🎓 Certificação GRÁTIS:
- [dbt Fundamentals (curso oficial grátis + certificado)](https://courses.getdbt.com/)
- Leva 1-2 semanas, é o primeiro certificado pro currículo!

---

---

# 📦 MÓDULO 5: Plataformas de Dados

## O que tu vai aprender:
- 🆕 Pipelines end-to-end com Bruin
- 🆕 Ingestão, transformação e qualidade de dados
- 🆕 Deploy em cloud (BigQuery)

## 📺 Vídeos:
- Material na pasta: [05-data-platforms/](05-data-platforms/)

---

---

# 📦 MÓDULO 6: Processamento em Lote (Apache Spark)

## O que tu vai aprender:
- 🆕 Apache Spark (processamento distribuído de dados grandes)
- 🆕 PySpark (Spark com Python)
- 🆕 DataFrames e SQL no Spark
- 🆕 Como funciona GroupBy e Joins internamente

## 📺 Vídeos:
- Material na pasta: [06-batch/](06-batch/)

## 💡 Conceito-chave:
> **Spark** = quando teus dados são grandes demais pro PostgreSQL (milhões/bilhões de linhas). Spark distribui o processamento em vários computadores. Netflix, Uber, Spotify usam Spark.

---

---

# 📦 MÓDULO 7: Streaming (Apache Kafka)

## O que tu vai aprender:
- 🆕 Apache Kafka (dados em tempo real)
- 🆕 Kafka Streams e KSQL
- 🆕 Schema management com Avro

## 📺 Vídeos:
- Material na pasta: [07-streaming/](07-streaming/)

## 💡 Conceito-chave:
> **Streaming** = processar dados ENQUANTO eles chegam (tempo real). Tu já faz isso com o bot de crypto! Kafka é a ferramenta enterprise pra isso. WhatsApp, Uber, LinkedIn usam Kafka.

---

---

# 🏆 PROJETO FINAL

## O que é:
Aplicar TUDO que aprendeu num projeto real completo:
- Ingestão de dados (API ou arquivo)
- Armazenamento (Data Warehouse)
- Transformação (dbt ou Spark)
- Orquestração (Kestra/Airflow)
- Dashboard/visualização

## 💡 Ideia pro TEU projeto final:
> **Pipeline de dados do teu bot de crypto:**
> API Binance → Ingestão com Python → BigQuery → dbt transforma → Dashboard com métricas de trading
>
> Isso usa TODOS os módulos e é um projeto REAL (não fictício) — destaque no portfólio!

---

---

# 📅 CRONOGRAMA SUGERIDO (self-paced)

| Semana | O que fazer |
|--------|-------------|
| 1 | Módulo 1: Docker (revisão rápida, tu já sabe) + Terraform (novo) |
| 2 | Módulo 1: Terraform + GCP + Homework |
| 3 | Módulo 2: Orquestração com Kestra |
| 4 | Workshop: Ingestão de dados com dlt |
| 5 | Módulo 3: BigQuery + Data Warehouse |
| 6 | Módulo 4: dbt (+ fazer certificação grátis) |
| 7 | Módulo 5: Plataformas de Dados (Bruin) |
| 8 | Módulo 6: Apache Spark |
| 9 | Módulo 7: Kafka Streaming |
| 10-12 | Projeto Final |

---

---

# 🔗 LINKS IMPORTANTES

| Recurso | URL |
|---------|-----|
| Playlist YouTube (todos os vídeos) | https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb |
| Comunidade Slack | https://datatalks.club/slack.html |
| Certificação dbt (grátis) | https://courses.getdbt.com/ |
| GCP Free Tier ($300 crédito) | https://cloud.google.com/free |
| AWS Free Tier (12 meses) | https://aws.amazon.com/free/ |
| Azure Free ($200 crédito) | https://azure.microsoft.com/free/ |
| Databricks Community (grátis) | https://community.cloud.databricks.com/ |

---

---

# ✅ CHECKLIST DE PROGRESSO

- [ ] **Módulo 1:** Docker + Terraform
  - [ ] Assistir vídeos 1.1 a 1.7
  - [ ] Fazer exercício (homework)
  - [ ] Criar conta GCP
  - [ ] Instalar Terraform
- [ ] **Módulo 2:** Orquestração
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Workshop 1:** Ingestão de dados
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Módulo 3:** Data Warehouse
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Módulo 4:** dbt
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
  - [ ] Certificação dbt Fundamentals (grátis!)
- [ ] **Módulo 5:** Plataformas de Dados
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Módulo 6:** Spark
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Módulo 7:** Kafka
  - [ ] Assistir vídeos
  - [ ] Fazer exercício
- [ ] **Projeto Final**
  - [ ] Definir tema
  - [ ] Implementar pipeline completo
  - [ ] Documentar no GitHub

---

*Guia criado para Israel Villaça — Agosto/2026*
*Baseado no [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (gratuito e open source)*
