# 🏛️ Janaseva – Multilingual WhatsApp Government Service Assistant

Janaseva is a production-ready, autonomous, multilingual WhatsApp assistant built to empower ordinary citizens in Kerala and India to seamlessly navigate and access verified information regarding government services in **Malayalam, English, and Manglish**.

---

## 🌟 Key Features

- **🌐 Multilingual Support**: First interaction presents language choice (Malayalam vs English) stored permanently. Understands Malayalam (`ലൈസൻസ് പുതുക്കണം`), Manglish (`license puthukkanam`), and English (`renew driving licence`).
- **🛡️ Strict AI Guardrails (Zero Hallucination)**: Gemini AI handles intent classification and language detection, while **100% of factual data** (required documents, fees, processing time, official links, step-by-step guides) is strictly sourced from PostgreSQL database records.
- **🏛️ 17 Pre-populated Government Services**: Pre-loaded with verified Kerala & India government service data:
  1. Driving Licence Renewal
  2. New Driving Licence
  3. Learner's Licence
  4. Aadhaar Card Update
  5. PAN Card
  6. Passport
  7. Birth Certificate
  8. Death Certificate
  9. Income Certificate
  10. Community Certificate
  11. Residence Certificate
  12. Ration Card
  13. Voter ID
  14. Pension Schemes (Old Age / Disability)
  15. Welfare Schemes (Karunya / KSRTC Concession)
  16. Vehicle Registration
  17. Vehicle Transfer
- **📋 Document Readiness Checker**: Interactive multi-turn checklist ("Do you have Aadhaar?", "Do you have Old Licence?") providing missing requirements or "You are ready to apply."
- **🎙️ Voice Note Support**: Accepts WhatsApp audio voice notes in Malayalam and English speech, converting to text and returning natural responses.
- **🖥️ React Admin Dashboard**: Complete web administration panel for adding/editing services, managing documents, FAQs, guides, and monitoring real-time analytics.
- **📱 Live WhatsApp Simulator**: Built-in interactive phone simulator on the web dashboard to test user flows end-to-end without external webhooks.
- **🐳 Full Docker & Nginx Setup**: One-click deployment with PostgreSQL 15, Redis 7, FastAPI, React, and Nginx.

---

## 🚀 Quick Start (Local Standalone Execution)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate

pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```
- **API Documentation**: Open `http://localhost:8000/docs`

### 2. Frontend Admin & Simulator Setup
```bash
cd frontend
npm install
npm run dev
```
- **Admin Dashboard & Simulator**: Open `http://localhost:3000` (Default credentials: `admin` / `janaseva123!`)

---

## 🐳 Production Deployment with Docker Compose

```bash
docker-compose up -d --build
```
This launches:
- **Nginx Reverse Proxy**: `http://localhost:80`
- **FastAPI Backend**: `http://localhost:8000`
- **PostgreSQL Database**: `localhost:5432`
- **Redis Cache**: `localhost:6379`

---

## 🧪 Running Pytest Test Suite

```bash
cd backend
python -m pytest tests/ -v --cov=app
```

---

## 📚 Documentation Reference
- [Architecture & Guardrails](docs/ARCHITECTURE.md)
- [Database Schema](docs/DATABASE.md)
- [API & Webhook Documentation](docs/API.md)
- [Production Deployment Guide](docs/DEPLOYMENT.md)
- [Admin User Manual](docs/ADMIN_GUIDE.md)
- [User Guide](docs/USER_GUIDE.md)
- [Troubleshooting & Logs](docs/TROUBLESHOOTING.md)
