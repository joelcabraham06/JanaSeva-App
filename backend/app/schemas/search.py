from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class SearchQueryRequest(BaseModel):
    query: str
    user_phone: Optional[str] = "910000000000"
    language: Optional[str] = None # 'ml', 'en', or None (auto-detect)

class SearchResultItem(BaseModel):
    id: int
    slug: str
    category: str
    name_en: str
    name_ml: str
    description_en: str
    description_ml: str
    score: float

class SearchQueryResponse(BaseModel):
    query: str
    detected_language: str
    resolved_intent: str
    matched_services: List[SearchResultItem]
    formatted_answer: str
