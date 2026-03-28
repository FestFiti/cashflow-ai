#!/bin/bash
set -euo pipefail

# CashFlow AI — SSL Setup via Let's Encrypt
# Usage: ./deploy/03-ssl.sh cashflow.yourdomain.com

DOMAIN="${1:?Usage: ./deploy/03-ssl.sh <domain>}"
SERVER="root@173.212.245.66"
SSH_KEY="$HOME/.ssh/contabo_mail"

echo "==> Setting up SSL for $DOMAIN"

ssh -i "$SSH_KEY" "$SERVER" bash -s -- "$DOMAIN" <<'REMOTE'
set -euo pipefail
DOMAIN="$1"

echo "[1/3] Installing certbot..."
apt-get install -y -qq certbot python3-certbot-nginx

echo "[2/3] Obtaining certificate for $DOMAIN..."
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email admin@"$DOMAIN" --redirect

echo "[3/3] Setting up auto-renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

echo ""
echo "==> SSL configured for $DOMAIN"
echo "    Certificate auto-renews via certbot timer"
REMOTE
