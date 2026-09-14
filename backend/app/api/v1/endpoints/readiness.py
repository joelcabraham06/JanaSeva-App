from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, UserPreference
from app.models.service import Service
from app.services.readiness_service import readiness_service

router = APIRouter()

class StartReadinessRequest(BaseModel):
    phone_number: str
    service_id: int
    language: Optional[str] = "ml"

class AnswerReadinessRequest(BaseModel):
    phone_number: str
    answer_yes: bool

@router.post("/start")
def start_readiness_check(payload: StartReadinessRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if not user:
        user = User(phone_number=payload.phone_number, preferred_language=payload.language or "ml")
        db.add(user)
        db.commit()
        db.refresh(user)

    service = db.query(Service).filter(Service.id == payload.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    prompt, buttons = readiness_service.start_readiness_check(db, user, service)
    return {"prompt": prompt, "buttons": buttons}

@router.post("/answer")
def answer_readiness_step(payload: AnswerReadinessRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prompt, buttons = readiness_service.process_answer(db, user, payload.answer_yes)
    return {"prompt": prompt, "buttons": buttons}
