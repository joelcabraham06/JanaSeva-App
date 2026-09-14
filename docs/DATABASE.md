# 🗄️ Database Schema Documentation

## Database Overview
Janaseva uses PostgreSQL (or SQLite in local dev) with SQLAlchemy ORM.

### Tables Summary

1. `users`: Stores user WhatsApp phone numbers and preferred language (`ml` or `en`).
2. `user_preferences`: Tracks session state (`IDLE`, `SELECT_LANG`, `READINESS_CHECK`), active service ID, and readiness checklist answers.
3. `services`: Contains core service records (slug, category, name_en, name_ml, description_en, description_ml, application_fee, processing_time_days, official_website, office_type, aliases_manglish).
4. `service_documents`: Associated mandatory and optional documents per service.
5. `service_guides`: Step-by-step walkthrough guides per service.
6. `service_faqs`: Frequently asked questions and verified answers per service.
7. `conversation_logs`: Complete log of raw queries, detected languages, resolved intents, and bot responses.
8. `voice_message_logs`: Audio file transcriptions and confidence metrics.
9. `intent_history`: Query-to-intent resolution stats.
10. `daily_metrics`: Aggregated daily request counts and language usage statistics.
11. `service_request_stats`: Counts per service requested by citizens.
12. `failed_search_logs`: Log of queries that failed to match existing services.
13. `satisfaction_feedbacks`: User feedback and star ratings.
14. `admin_users`: Administrator credentials and roles.
15. `audit_logs`: Security log of administrative updates.
