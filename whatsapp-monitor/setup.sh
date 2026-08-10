#!/bin/bash
# =============================================
# 🚀 SETUP AUTOMÁTICO - Monitor WhatsApp
# Evolution API + Chatwoot
# =============================================

set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  📱 Monitor WhatsApp - Setup Automático  ║"
echo "║  Evolution API + Chatwoot                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se é root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Execute como root: sudo ./setup.sh${NC}"
    exit 1
fi

# ============================================
# 1. INSTALAR DEPENDÊNCIAS
# ============================================
echo -e "${YELLOW}📦 [1/7] Verificando dependências...${NC}"

if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker instalado${NC}"
else
    echo -e "${GREEN}✅ Docker já instalado ($(docker --version))${NC}"
fi

if ! docker compose version &> /dev/null; then
    echo "Instalando Docker Compose plugin..."
    apt-get install -y docker-compose-plugin
    echo -e "${GREEN}✅ Docker Compose instalado${NC}"
else
    echo -e "${GREEN}✅ Docker Compose já instalado${NC}"
fi

# ============================================
# 2. GERAR CREDENCIAIS
# ============================================
echo ""
echo -e "${YELLOW}🔑 [2/7] Gerando credenciais seguras...${NC}"

POSTGRES_PASS=$(openssl rand -base64 24 | tr -d '=/+' | head -c 32)
REDIS_PASS=$(openssl rand -base64 24 | tr -d '=/+' | head -c 32)
SECRET_KEY=$(openssl rand -hex 64)
API_KEY=$(cat /proc/sys/kernel/random/uuid)

echo -e "${GREEN}✅ Credenciais geradas${NC}"

# ============================================
# 3. DETECTAR IP
# ============================================
echo ""
echo -e "${YELLOW}🌐 [3/7] Detectando IP público...${NC}"

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "localhost")
echo -e "${GREEN}✅ IP detectado: ${PUBLIC_IP}${NC}"

# ============================================
# 4. CRIAR .ENV
# ============================================
echo ""
echo -e "${YELLOW}📝 [4/7] Criando arquivo .env...${NC}"

cat > .env << EOF
# =============================================
# GERADO AUTOMATICAMENTE POR setup.sh
# Data: $(date '+%Y-%m-%d %H:%M:%S')
# =============================================

# --- POSTGRESQL ---
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${POSTGRES_PASS}

# --- REDIS ---
REDIS_PASSWORD=${REDIS_PASS}

# --- EVOLUTION API ---
EVOLUTION_SERVER_URL=http://${PUBLIC_IP}:8080
EVOLUTION_API_KEY=${API_KEY}

# --- CHATWOOT ---
SECRET_KEY_BASE=${SECRET_KEY}
CHATWOOT_FRONTEND_URL=http://${PUBLIC_IP}:3000
CHATWOOT_ACCOUNT_ID=1
CHATWOOT_TOKEN=PREENCHER_DEPOIS
CHATWOOT_URL=http://chatwoot-rails:3000

# --- EMAIL (configurar depois) ---
MAILER_SENDER_EMAIL=noreply@localhost
SMTP_DOMAIN=localhost
SMTP_ADDRESS=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
EOF

echo -e "${GREEN}✅ .env criado${NC}"

# ============================================
# 5. SUBIR CONTAINERS
# ============================================
echo ""
echo -e "${YELLOW}🐳 [5/7] Subindo containers (pode levar 3-5 min na primeira vez)...${NC}"

docker compose pull
docker compose up -d

echo -e "${GREEN}✅ Containers iniciados${NC}"

# ============================================
# 6. AGUARDAR SERVIÇOS
# ============================================
echo ""
echo -e "${YELLOW}⏳ [6/7] Aguardando serviços ficarem prontos...${NC}"

# Aguardar PostgreSQL
echo -n "  PostgreSQL..."
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -U postgres &>/dev/null; then
        echo -e " ${GREEN}OK${NC}"
        break
    fi
    sleep 2
    echo -n "."
done

# Aguardar Redis
echo -n "  Redis..."
for i in {1..15}; do
    if docker compose exec -T redis redis-cli -a "${REDIS_PASS}" ping &>/dev/null; then
        echo -e " ${GREEN}OK${NC}"
        break
    fi
    sleep 2
    echo -n "."
done

# Preparar banco Chatwoot
echo "  Preparando banco do Chatwoot (pode levar 1-2 min)..."
sleep 10
docker compose exec -T chatwoot-rails bundle exec rails db:chatwoot_prepare 2>/dev/null || \
docker compose exec -T chatwoot-rails bundle exec rails db:chatwoot_prepare 2>/dev/null || \
echo -e "  ${YELLOW}⚠️  Se der erro, rode manualmente: docker compose exec chatwoot-rails bundle exec rails db:chatwoot_prepare${NC}"

echo -e "${GREEN}✅ Serviços prontos${NC}"

# ============================================
# 7. RESUMO FINAL
# ============================================
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║               🎉 INSTALAÇÃO CONCLUÍDA!                  ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                                                          ║"
echo "║  📊 Chatwoot (Painel):                                   ║"
echo "║     http://${PUBLIC_IP}:3000                              "
echo "║                                                          ║"
echo "║  🔌 Evolution API (Manager):                             ║"
echo "║     http://${PUBLIC_IP}:8080/manager                      "
echo "║                                                          ║"
echo "║  🔑 Evolution API Key:                                   ║"
echo "║     ${API_KEY}                                            "
echo "║                                                          ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                                                          ║"
echo "║  📋 PRÓXIMOS PASSOS:                                     ║"
echo "║                                                          ║"
echo "║  1. Acesse o Chatwoot e crie sua conta admin             ║"
echo "║  2. Acesse o Evolution Manager com a API Key acima       ║"
echo "║  3. Crie uma instância (ex: vendedor-joao)               ║"
echo "║  4. Escaneie o QR Code com o celular do vendedor         ║"
echo "║  5. As conversas começam a aparecer no Chatwoot!         ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: Salve essas credenciais num lugar seguro!${NC}"
echo ""
echo "  PostgreSQL Password: ${POSTGRES_PASS}"
echo "  Redis Password:      ${REDIS_PASS}"
echo "  Evolution API Key:   ${API_KEY}"
echo "  Chatwoot Secret:     ${SECRET_KEY:0:20}..."
echo ""
echo -e "${GREEN}Credenciais também salvas no arquivo .env${NC}"
echo ""

# Salvar credenciais em arquivo separado (segurança)
cat > .credentials << EOF
# =============================================
# CREDENCIAIS - MANTER EM LOCAL SEGURO
# Gerado em: $(date '+%Y-%m-%d %H:%M:%S')
# =============================================

PostgreSQL Password: ${POSTGRES_PASS}
Redis Password:      ${REDIS_PASS}
Evolution API Key:   ${API_KEY}
Chatwoot Secret:     ${SECRET_KEY}

Chatwoot URL:        http://${PUBLIC_IP}:3000
Evolution URL:       http://${PUBLIC_IP}:8080
Evolution Manager:   http://${PUBLIC_IP}:8080/manager
EOF

chmod 600 .credentials
echo -e "📄 Credenciais salvas em: ${GREEN}.credentials${NC} (chmod 600)"
echo ""
