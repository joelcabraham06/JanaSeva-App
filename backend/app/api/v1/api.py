from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    services,
    documents,
    faqs,
    guides,
    search,
    readiness,
    webhook,
    voice,
    analytics,
    admin
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(services.router, prefix="/services", tags=["Services Management"])
api_router.include_router(documents.router, prefix="/documents", tags=["Service Documents"])
api_router.include_router(faqs.router, prefix="/faqs", tags=["Service FAQs"])
api_router.include_router(guides.router, prefix="/guides", tags=["Service Guides"])
api_router.include_router(search.router, prefix="/search", tags=["Search & Intent"])
api_router.include_router(readiness.router, prefix="/readiness", tags=["Readiness Checker"])
api_router.include_router(webhook.router, prefix="/webhook", tags=["WhatsApp Webhook"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice Processing"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics Dashboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin & Audit Logs"])
