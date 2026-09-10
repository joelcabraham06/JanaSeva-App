from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class UserBase(BaseModel):
    phone_number: str
    preferred_language: str = "ml"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True

class UserPreferenceUpdate(BaseModel):
    session_state: Optional[str] = None
    active_service_id: Optional[int] = None
    readiness_answers: Optional[Dict[str, Any]] = None
    current_step_index: Optional[int] = None
