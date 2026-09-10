from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.session import Base

class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input_type = Column(String(20), default="text") # 'text', 'voice', 'button'
    raw_input = Column(Text, nullable=False)
    detected_language = Column(String(10), nullable=True) # 'en', 'ml', 'manglish'
    resolved_intent = Column(String(100), nullable=True)
    response_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="conversations")

class VoiceMessageLog(Base):
    __tablename__ = "voice_message_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    media_id = Column(String(100), nullable=True)
    file_path = Column(String(300), nullable=True)
    transcription = Column(Text, nullable=True)
    detected_language = Column(String(10), default="ml")
    confidence = Column(Float, default=0.95)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class IntentHistory(Base):
    __tablename__ = "intent_history"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    resolved_service_id = Column(Integer, ForeignKey("services.id", ondelete="SET NULL"), nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
