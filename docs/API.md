# 🔌 API & Webhook Specification

Interactive OpenAPI Swagger UI is available at `/docs` when the backend is running.

## Key Endpoints Summary

### Authentication
- `POST /api/v1/auth/login`: Admin login returning JWT bearer token.
- `GET /api/v1/auth/me`: Get current admin details.

### Services Management
- `GET /api/v1/services/`: List all active services.
- `POST /api/v1/services/`: Create a new government service (Admin).
- `PUT /api/v1/services/{id}`: Update service details (Admin).
- `DELETE /api/v1/services/{id}`: Deactivate a service (Admin).

### Multilingual Search
- `POST /api/v1/search/query`: Execute Malayalam, English, or Manglish search.

### WhatsApp Webhook
- `GET /api/v1/webhook/whatsapp`: Meta webhook verification.
- `POST /api/v1/webhook/whatsapp`: Incoming Meta WhatsApp Cloud API webhook handler.
- `POST /api/v1/webhook/simulator`: Interactive Web WhatsApp Simulator for local testing.

### Voice STT Processing
- `POST /api/v1/voice/process`: Transcribe audio voice note and execute search.

### Analytics & Audit
- `GET /api/v1/analytics/dashboard`: Retrieve aggregated usage metrics.
- `GET /api/v1/admin/audit-logs`: Audit logs of administrative changes.
