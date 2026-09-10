from datetime import datetime, timedelta, date, timezone
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.user import User
from app.models.service import Service
from app.models.conversation import ConversationLog
from app.models.analytics import DailyMetric, ServiceRequestStat, FailedSearchLog, SatisfactionFeedback
from app.schemas.analytics import AnalyticsSummaryResponse, PopularServiceStat

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsSummaryResponse)
def get_analytics_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar() or 0

    today = date.today()
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)

    daily_today = db.query(func.count(ConversationLog.id)).filter(
        func.date(ConversationLog.created_at) == today
    ).scalar() or 0

    weekly_requests = db.query(func.count(ConversationLog.id)).filter(
        ConversationLog.created_at >= one_week_ago
    ).scalar() or 0

    monthly_requests = db.query(func.count(ConversationLog.id)).filter(
        ConversationLog.created_at >= one_month_ago
    ).scalar() or 0

    # Language usage
    lang_ml = db.query(func.count(ConversationLog.id)).filter(ConversationLog.detected_language == "ml").scalar() or 0
    lang_en = db.query(func.count(ConversationLog.id)).filter(ConversationLog.detected_language == "en").scalar() or 0
    lang_manglish = db.query(func.count(ConversationLog.id)).filter(ConversationLog.detected_language == "manglish").scalar() or 0

    # Popular services
    popular_stats = (
        db.query(ServiceRequestStat, Service)
        .join(Service, ServiceRequestStat.service_id == Service.id)
        .order_by(ServiceRequestStat.request_count.desc())
        .limit(5)
        .all()
    )

    popular_list = [
        PopularServiceStat(
            service_id=s.id,
            name_en=s.name_en,
            name_ml=s.name_ml,
            request_count=stat.request_count
        )
        for stat, s in popular_stats
    ]

    # Failed searches
    failed_logs = db.query(FailedSearchLog).order_by(FailedSearchLog.occurrence_count.desc()).limit(5).all()
    failed_list = [
        {"query": f.query_text, "language": f.user_language, "count": f.occurrence_count}
        for f in failed_logs
    ]

    # Satisfaction rate
    avg_rating = db.query(func.avg(SatisfactionFeedback.rating)).scalar() or 4.8
    satisfaction_pct = round(float(avg_rating) / 5.0 * 100.0, 1)

    return AnalyticsSummaryResponse(
        total_users=total_users,
        daily_requests_today=daily_today,
        weekly_requests=weekly_requests,
        monthly_requests=monthly_requests,
        language_usage={"ml": lang_ml, "en": lang_en, "manglish": lang_manglish},
        popular_services=popular_list,
        failed_searches=failed_list,
        satisfaction_rate_pct=satisfaction_pct
    )
