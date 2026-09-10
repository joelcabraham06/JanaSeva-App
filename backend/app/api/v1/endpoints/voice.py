import base64
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.stt_service import stt_service
from app.api.v1.endpoints.webhook import _process_whatsapp_message
from app.models.conversation import VoiceMessageLog
from app.models.user import User

router = APIRouter()

class VoiceBase64Request(BaseModel):
    phone_number: str = "919876543210"
    audio_base64: str
    mime_type: str = "audio/ogg"

@router.post("/process")
async def process_voice_message(
    payload: VoiceBase64Request,
    db: Session = Depends(get_db)
):
    """
    Processes incoming WhatsApp audio voice notes (base64 payload).
    Transcribes Malayalam/English speech and routes through search intent engine.
    """
    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 audio data: {e}")

    transcription, detected_lang = stt_service.transcribe_audio(audio_bytes, payload.mime_type)

    user = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if user:
        db.add(
            VoiceMessageLog(
                user_id=user.id,
                transcription=transcription,
                detected_language=detected_lang,
                confidence=0.95
            )
        )
        db.commit()

    reply_text, buttons, lang = await _process_whatsapp_message(
        db, payload.phone_number, transcription, "voice"
    )

    return {
        "status": "success",
        "transcription": transcription,
        "detected_language": detected_lang,
        "reply_text": reply_text,
        "interactive_buttons": buttons
    }
