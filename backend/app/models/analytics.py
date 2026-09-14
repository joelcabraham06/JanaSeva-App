from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Float

from app.db.session import Base

class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(Date, unique=True, default=date.today)
    total_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    total_requests = Column(Integer, default=0)
    voice_requests = Column(Integer, default=0)
    malayalam_queries = Column(Integer, default=0)
    english_queries = Column(Integer, default=0)
    manglish_queries = Column(Integer, default=0)

class ServiceRequestStat(Base):
    __tablename__ = "service_request_stats"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    request_count = Column(Integer, default=1)
    last_requested = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class FailedSearchLog(Base):
    __tablename__ = "failed_search_logs"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    user_language = Column(String(10), default="ml")
    occurrence_count = Column(Integer, default=1)
    last_attempted = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class SatisfactionFeedback(Base):
    __tablename__ = "satisfaction_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False) # 1 to 5 stars or binary 1/0
    feedback_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
