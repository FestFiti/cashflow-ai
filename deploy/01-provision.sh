#!/bin/bash
set -euo pipefail

# CashFlow AI — Server Provisioning Script
# Installs Docker, Docker Compose, nginx, and sets up the deployment directory
# Usage: ./deploy/01-provision.sh

SERVER="root@173.212.245.66"
SSH_KEY="$HOME/.ssh/contabo_mail"
DEPLOY_DIR="/opt/cashflow-ai"

echo "==> Provisioning server at $SERVER"
echo "    SSH key: $SSH_KEY"
echo ""

ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail

echo "[1/6] Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

echo "[2/6] Installing prerequisites..."
apt-get install -y -qq \
    ca-certificates curl gnupg lsb-release \
    ufw git

echo "[3/6] Installing Docker..."
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo "  Docker installed: $(docker --version)"
else
    echo "  Docker already installed: $(docker --version)"
fi

echo "[4/6] Installing Docker Compose plugin..."
if ! docker compose version &>/dev/null; then
    apt-get install -y -qq docker-compose-plugin
    echo "  Docker Compose installed: $(docker compose version)"
else
    echo "  Docker Compose already installed: $(docker compose version)"
fi

echo "[5/6] Installing nginx..."
if ! command -v nginx &>/dev/null; then
    apt-get install -y -qq nginx
    systemctl enable nginx
    systemctl start nginx
    echo "  nginx installed: $(nginx -v 2>&1)"
else
    echo "  nginx already installed: $(nginx -v 2>&1)"
fi

echo "[6/6] Creating deployment directory..."
mkdir -p /opt/cashflow-ai
mkdir -p /opt/cashflow-ui

echo ""
echo "==> Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8888/tcp
ufw allow 9999/tcp
ufw --force enable

echo ""
echo "==> Provisioning complete!"
echo "    Docker: $(docker --version)"
echo "    Compose: $(docker compose version)"
echo "    nginx: $(nginx -v 2>&1)"
echo "    Deploy dir: /opt/cashflow-ai"
echo "    UI dir: /opt/cashflow-ui"
REMOTE

echo ""
echo "==> Server provisioned successfully!"
echo "    Next: ./deploy/02-deploy.sh"
