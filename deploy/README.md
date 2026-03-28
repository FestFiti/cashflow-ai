# Deployment Guide — CashFlow AI

Multi-step deployment to Contabo server at `173.212.245.66`.

## Prerequisites
- SSH access: `ssh -i ~/.ssh/contabo_mail root@173.212.245.66`
- Domain pointed to server IP (or use IP directly)

## Steps

```bash
# 1. Provision the server (install Docker, nginx, etc.)
./deploy/01-provision.sh

# 2. Deploy the application
./deploy/02-deploy.sh

# 3. (Optional) Set up SSL with Let's Encrypt
./deploy/03-ssl.sh cashflow.yourdomain.com
```

## Ports
- **8888** — Backend API (FastAPI)
- **9999** — Frontend dev (or served via nginx in production)
- **80/443** — nginx reverse proxy (production)

## Update Deployment
```bash
./deploy/02-deploy.sh
```
This rebuilds and restarts all services on the server.
