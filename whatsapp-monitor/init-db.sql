-- Cria banco separado para Evolution API
CREATE DATABASE evolution;

-- Grants
GRANT ALL PRIVILEGES ON DATABASE evolution TO postgres;
GRANT ALL PRIVILEGES ON DATABASE chatwoot_production TO postgres;
