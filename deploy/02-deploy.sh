#!/bin/bash
set -euo pipefail

# CashFlow AI — Deployment Script
# Builds locally, copies to server, runs with Docker Compose
# Usage: ./deploy/02-deploy.sh

SERVER="root@173.212.245.66"
SSH_KEY="$HOME/.ssh/contabo_mail"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEPLOY_DIR="/opt/cashflow-ai"
UI_DIR="/opt/cashflow-ui"

echo "==> Deploying CashFlow AI"
echo "    Project: $PROJECT_DIR"
echo "    Server:  $SERVER"
echo ""

# ---- Step 1: Build frontend ----
echo "[1/5] Building frontend..."
cd "$PROJECT_DIR/frontend"
npm install --silent
npm run build
echo "  Frontend built successfully"

# ---- Step 2: Sync backend to server ----
echo "[2/5] Syncing backend to server..."
rsync -az --delete \
    -e "ssh -i $SSH_KEY" \
    --exclude='__pycache__' \
    --exclude='.env' \
    --exclude='*.pyc' \
    --exclude='venv' \
    "$PROJECT_DIR/backend/" \
    "$SERVER:$DEPLOY_DIR/backend/"

# Copy docker-compose and env
scp -i "$SSH_KEY" "$PROJECT_DIR/docker-compose.yml" "$SERVER:$DEPLOY_DIR/"
scp -i "$SSH_KEY" "$PROJECT_DIR/deploy/nginx-cashflow.conf" "$SERVER:/etc/nginx/sites-available/cashflow-ai"

echo "  Backend synced"

# ---- Step 3: Deploy frontend static files ----
echo "[3/5] Deploying frontend build..."
rsync -az --delete \
    -e "ssh -i $SSH_KEY" \
    "$PROJECT_DIR/frontend/build/" \
    "$SERVER:$UI_DIR/"
echo "  Frontend deployed to $UI_DIR"

# ---- Step 4: Start services on server ----
echo "[4/5] Starting services on server..."
ssh -i "$SSH_KEY" "$SERVER" bash -s <<REMOTE
set -euo pipefail

cd $DEPLOY_DIR

# Create .env if it doesn't exist
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "  Created .env from .env.example — UPDATE WITH REAL VALUES"
fi

# Build and start containers
docker compose up -d --build

echo "  Services started"
docker compose ps
REMOTE

# ---- Step 5: Configure nginx ----
echo "[5/5] Configuring nginx..."
ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail

# Enable the site
ln -sf /etc/nginx/sites-available/cashflow-ai /etc/nginx/sites-enabled/cashflow-ai

# Remove default if it exists
rm -f /etc/nginx/sites-enabled/default

# Test and reload
nginx -t
systemctl reload nginx

echo "  nginx configured and reloaded"
REMOTE

echo ""
echo "==> Deployment complete!"
echo "    API:       http://173.212.245.66:8888"
echo "    API Docs:  http://173.212.245.66:8888/docs"
echo "    Frontend:  http://173.212.245.66"
echo ""
echo "    Remember to update backend/.env on the server with real API keys!"
