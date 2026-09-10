# 🛠️ Troubleshooting & Diagnostics Guide

## Common Issues & Solutions

### 1. Database Connection Failure
**Symptom**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Fix**: Verify PostgreSQL service status or check `.env` DATABASE_URL format. If using SQLite fallback, ensure directory write permissions.

### 2. WhatsApp Webhook Token Mismatch
**Symptom**: `403 Forbidden: Verification token mismatch`
**Fix**: Ensure `WHATSAPP_VERIFY_TOKEN` in `.env` matches the verify token entered in Meta Developer Dashboard.

### 3. Gemini API Key Missing / Rate Limited
**Symptom**: `Gemini API intent resolution fallback triggered`
**Fix**: Check `GEMINI_API_KEY` in `.env`. Note that Janaseva automatically falls back to regex and local dictionary matching if Gemini API is unreachable, ensuring continuous uptime.

## Log Inspection
```bash
# Docker logs
docker-compose logs -f backend

# Pytest execution
cd backend
python -m pytest tests/ -v
```
