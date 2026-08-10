# 📱 Monitor WhatsApp — Evolution API + Chatwoot

> Sistema de monitoramento centralizado de conversas WhatsApp para equipe de vendas.
> Todas as mensagens ficam salvas mesmo se o vendedor deletar no celular.

---

## 🎯 O que esse sistema faz

- ✅ Conecta até **5+ números de WhatsApp** (vendedores)
- ✅ **Salva todas as conversas** em banco de dados (backup permanente)
- ✅ **Se deletar no celular** → continua salvo na plataforma
- ✅ **Painel web** para ver todas as conversas em tempo real
- ✅ **Filtro por vendedor** (cada número = 1 inbox)
- ✅ **Busca** em mensagens antigas
- ✅ **Relatórios** de volume, tempo de resposta, etc.
- ✅ Vendedor **continua usando o celular normalmente**

---

## 🏗️ Arquitetura

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Vendedor 1 │────▶│                 │     │              │
│  (celular)  │     │                 │     │   CHATWOOT   │
├─────────────┤     │  EVOLUTION API  │────▶│   (Painel)   │
│  Vendedor 2 │────▶│                 │     │              │
│  (celular)  │     │  Conecta via    │     │  Todas as    │
├─────────────┤     │  WhatsApp Web   │     │  conversas   │
│  Vendedor 3 │────▶│  (QR Code)      │     │  ficam aqui  │
│  (celular)  │     │                 │     │              │
├─────────────┤     │  Captura TUDO:  │     │  Dono vê     │
│  Vendedor 4 │────▶│  - Enviadas     │     │  tudo em     │
│  (celular)  │     │  - Recebidas    │     │  tempo real  │
├─────────────┤     │  - Deletadas    │     │              │
│  Vendedor 5 │────▶│  - Mídia        │     │              │
│  (celular)  │     │                 │     │              │
└─────────────┘     └─────────────────┘     └──────────────┘
                            │
                    ┌───────┴───────┐
                    │  PostgreSQL   │  ← Tudo salvo aqui
                    │  + Redis      │
                    └───────────────┘
```

---

## 📋 Pré-requisitos

| Item | Mínimo | Recomendado |
|------|--------|-------------|
| **VPS** | 2 vCPU, 4GB RAM | 4 vCPU, 8GB RAM |
| **SO** | Ubuntu 22.04+ | Ubuntu 24.04 |
| **Docker** | v24+ | v25+ |
| **Docker Compose** | v2.20+ | v2.27+ |
| **Disco** | 20GB SSD | 50GB SSD |
| **Porta** | 3000, 8080 abertas | + 80/443 com Nginx |

### VPS recomendadas (custo-benefício):
- **Hetzner** — €4.5/mês (CX22: 2vCPU, 4GB) ⭐ melhor custo
- **Contabo** — €6/mês (4vCPU, 8GB)
- **DigitalOcean** — $12/mês (2vCPU, 4GB)
- **Railway** — ~$10-15/mês (auto-scale)

---

## 🚀 Instalação Passo a Passo

### 1. Preparar a VPS

```bash
# Conectar na VPS via SSH
ssh root@SEU_IP_DA_VPS

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Instalar Docker Compose plugin
apt install docker-compose-plugin -y

# Verificar instalação
docker --version
docker compose version
```

### 2. Clonar o projeto

```bash
# Clonar repositório
git clone https://github.com/rhaelbit/meu-bot-telegram.git
cd meu-bot-telegram/whatsapp-monitor

# Ou se preferir criar do zero:
mkdir -p /opt/whatsapp-monitor && cd /opt/whatsapp-monitor
# (copie os arquivos docker-compose.yml, .env.example, init-db.sql)
```

### 3. Configurar variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas configurações
nano .env
```

**Variáveis OBRIGATÓRIAS para alterar:**

```bash
# Gerar senha PostgreSQL (copie o resultado)
openssl rand -base64 24

# Gerar senha Redis
openssl rand -base64 24

# Gerar SECRET_KEY_BASE do Chatwoot
openssl rand -hex 64

# Gerar API Key da Evolution (UUID)
cat /proc/sys/kernel/random/uuid
```

Preencha no `.env`:
```env
POSTGRES_PASSWORD=<senha gerada>
REDIS_PASSWORD=<senha gerada>
SECRET_KEY_BASE=<hex 64 gerado>
EVOLUTION_API_KEY=<uuid gerado>
EVOLUTION_SERVER_URL=http://SEU_IP:8080
CHATWOOT_FRONTEND_URL=http://SEU_IP:3000
```

### 4. Subir os containers

```bash
# Subir tudo (primeira vez demora 2-5 min pra baixar imagens)
docker compose up -d

# Verificar se tudo subiu
docker compose ps

# Deve mostrar todos os 5 containers "running":
# - monitor_postgres
# - monitor_redis
# - monitor_evolution
# - monitor_chatwoot
# - monitor_chatwoot_worker
```

### 5. Preparar banco do Chatwoot (APENAS primeira vez)

```bash
# Criar tabelas do Chatwoot
docker compose exec chatwoot-rails bundle exec rails db:chatwoot_prepare

# Se der erro, rode novamente (normal na primeira vez)
docker compose exec chatwoot-rails bundle exec rails db:chatwoot_prepare
```

### 6. Criar conta admin no Chatwoot

```bash
# Criar super admin
docker compose exec chatwoot-rails bundle exec rails console

# No console Rails, digite:
SuperAdmin.create!(email: 'admin@seudominio.com', password: 'SuaSenhaForte123!', name: 'Admin')
exit
```

**Ou acesse direto:** `http://SEU_IP:3000` — na primeira vez aparece tela de criação de conta.

### 7. Conectar na Evolution API

Acesse o Manager da Evolution:
```
http://SEU_IP:8080/manager
```

Login com a API Key que você definiu no `.env`.

### 8. Criar instâncias (uma por vendedor)

Na interface do Manager da Evolution, crie 5 instâncias:

| Instância | Nome sugerido |
|-----------|---------------|
| 1 | vendedor-joao |
| 2 | vendedor-maria |
| 3 | vendedor-pedro |
| 4 | vendedor-ana |
| 5 | vendedor-carlos |

**Para cada instância:**
1. Clique em "Create Instance"
2. Nome: `vendedor-joao` (por exemplo)
3. Ative a integração Chatwoot (preenche automaticamente se CHATWOOT_AUTO_CREATE=true)
4. Clique em "Connect" → aparece QR Code
5. **Vendedor escaneia o QR Code** no celular (WhatsApp > Aparelhos conectados > Conectar aparelho)
6. Pronto! Todas as mensagens desse número agora vão pro Chatwoot

### 9. Verificar no Chatwoot

1. Acesse `http://SEU_IP:3000`
2. Login com a conta admin criada
3. Vá em **Settings > Inboxes** — deve ter 5 inboxes (uma por vendedor)
4. As conversas começam a aparecer automaticamente

---

## ✅ Checklist pós-instalação

- [ ] Todos os 5 containers rodando (`docker compose ps`)
- [ ] Chatwoot acessível em `:3000`
- [ ] Evolution API acessível em `:8080`
- [ ] Admin criado no Chatwoot
- [ ] Instância de teste criada na Evolution
- [ ] QR Code escaneado com sucesso
- [ ] Mensagem de teste enviada e apareceu no Chatwoot
- [ ] Mensagem deletada no celular → continua no Chatwoot ✓

---

## 🔧 Comandos úteis

```bash
# Ver logs de todos os containers
docker compose logs -f

# Ver logs só da Evolution
docker compose logs -f evolution-api

# Ver logs só do Chatwoot
docker compose logs -f chatwoot-rails

# Reiniciar tudo
docker compose restart

# Parar tudo
docker compose down

# Parar e APAGAR dados (CUIDADO!)
docker compose down -v

# Ver uso de disco
docker system df

# Atualizar imagens
docker compose pull && docker compose up -d
```

---

## 🛡️ Segurança (produção)

### Configurar Nginx como proxy reverso (HTTPS):

```bash
# Instalar Nginx + Certbot
apt install nginx certbot python3-certbot-nginx -y
```

Criar `/etc/nginx/sites-available/monitor`:

```nginx
# Chatwoot
server {
    listen 80;
    server_name chat.seudominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Evolution API
server {
    listen 80;
    server_name api.seudominio.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
ln -s /etc/nginx/sites-available/monitor /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# SSL automático
certbot --nginx -d chat.seudominio.com -d api.seudominio.com
```

### Firewall:

```bash
# Permitir apenas SSH, HTTP, HTTPS
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# NÃO expor 5432 (postgres) e 6379 (redis) pro mundo!
# Remover do docker-compose.yml as portas em produção
```

---

## 🔄 Backup automático

Criar `/opt/whatsapp-monitor/backup.sh`:

```bash
#!/bin/bash
# Backup diário do banco de dados
BACKUP_DIR="/opt/backups/whatsapp-monitor"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Dump PostgreSQL
docker compose -f /opt/whatsapp-monitor/docker-compose.yml exec -T postgres \
  pg_dumpall -U postgres | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Manter apenas últimos 30 dias
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup concluído: db_$DATE.sql.gz"
```

```bash
# Tornar executável
chmod +x /opt/whatsapp-monitor/backup.sh

# Agendar backup diário às 3h da manhã
crontab -e
# Adicionar:
0 3 * * * /opt/whatsapp-monitor/backup.sh >> /var/log/monitor-backup.log 2>&1
```

---

## ❓ FAQ / Troubleshooting

### "QR Code não aparece"
- Verifique se a Evolution está rodando: `docker compose logs evolution-api`
- Verifique se o container tem internet: `docker compose exec evolution-api ping google.com`

### "Mensagens não aparecem no Chatwoot"
- Verifique a integração: na Evolution, a instância deve ter Chatwoot habilitado
- Verifique token: o `CHATWOOT_TOKEN` no `.env` deve ser o token do admin
- Logs: `docker compose logs chatwoot-rails | grep -i error`

### "Chatwoot dá erro 500"
- Rode migrations: `docker compose exec chatwoot-rails bundle exec rails db:migrate`
- Verifique SECRET_KEY_BASE (deve ter 64+ chars hex)

### "Vendedor desconectou"
- O vendedor pode ter desconectado o "aparelho conectado" no celular
- Reconecte: na Evolution, gere novo QR Code pra instância

### "Container reinicia em loop"
- Verifique logs: `docker compose logs <nome_container>`
- Geralmente é senha errada ou banco não criado

---

## 📊 Custos mensais estimados

| Item | Custo |
|------|-------|
| VPS (Hetzner CX22) | ~R$ 30/mês |
| Domínio (opcional) | ~R$ 40/ano |
| 5 chips pré-pago (se precisar) | R$ 75 (único) |
| Software | **R$ 0** (open source) |
| **Total mensal** | **~R$ 30-50/mês** |

---

## 🚀 Próximos passos (evolução)

1. **Fase 1 (atual):** Monitoramento + backup de conversas ✅
2. **Fase 2:** Bot IA de reativação de clientes (conecta ao mesmo sistema)
3. **Fase 3:** Integração com CRM/ERP (Microvix) para segmentação automática
4. **Fase 4:** Analítica preditiva (score de churn, recomendação de ação)

---

*Criado por Israel Villaça — Automação Comercial com IA*
*Última atualização: Agosto/2026*
