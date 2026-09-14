from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class PopularServiceStat(BaseModel):
    service_id: int
    name_en: str
    name_ml: str
    request_count: int

class AnalyticsSummaryResponse(BaseModel):
    total_users: int
    daily_requests_today: int
    weekly_requests: int
    monthly_requests: int
    language_usage: Dict[str, int] # {'ml': count, 'en': count, 'manglish': count}
    popular_services: List[PopularServiceStat]
    failed_searches: List[Dict[str, Any]]
    satisfaction_rate_pct: float
