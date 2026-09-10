# 🚀 Production Deployment Guide

## Prerequisites
- Server with Docker & Docker Compose installed.
- Domain name pointed to server IP.
- Meta Developer Account with WhatsApp Cloud API access.

## Step 1: Clone & Configure `.env`
```bash
cp .env.example .env
nano .env
```
Update credentials:
- `SECRET_KEY`: Set strong random 32-character string.
- `WHATSAPP_TOKEN`: Meta access token.
- `WHATSAPP_PHONE_NUMBER_ID`: Meta phone ID.
- `GEMINI_API_KEY`: Google Gemini API key.

## Step 2: Deploy Containers
```bash
docker-compose up -d --build
```

## Step 3: Configure Meta Webhook
1. Go to [Meta Developer Portal](https://developers.facebook.com/).
2. Under WhatsApp -> Configuration -> Webhook:
   - **Callback URL**: `https://yourdomain.com/api/v1/webhook/whatsapp`
   - **Verify Token**: `janaseva_verify_token` (matches `.env`)
3. Subscribe to `messages`.
