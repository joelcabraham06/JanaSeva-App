from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.session import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    
    # Multilingual Titles & Content
    name_en = Column(String(200), nullable=False)
    name_ml = Column(String(200), nullable=False)
    description_en = Column(Text, nullable=False)
    description_ml = Column(Text, nullable=False)
    eligibility_en = Column(Text, nullable=True)
    eligibility_ml = Column(Text, nullable=True)
    
    # Government metadata
    application_fee = Column(String(100), nullable=False, default="Free / Standard Fee")
    processing_time_days = Column(Integer, nullable=True, default=7)
    online_available = Column(Boolean, default=True)
    offline_available = Column(Boolean, default=True)
    official_website = Column(String(300), nullable=False)
    office_type = Column(String(150), nullable=False, default="Akshaya Center / RTO / Panchayat")
    source_url = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Keywords & Search aliases (JSON list stored as string or text)
    aliases_en = Column(Text, nullable=True)  # comma separated
    aliases_ml = Column(Text, nullable=True)  # comma separated
    aliases_manglish = Column(Text, nullable=True)  # comma separated

    documents = relationship("ServiceDocument", back_populates="service", cascade="all, delete-orphan")
    guides = relationship("ServiceGuide", back_populates="service", cascade="all, delete-orphan")
    faqs = relationship("ServiceFAQ", back_populates="service", cascade="all, delete-orphan")

class ServiceDocument(Base):
    __tablename__ = "service_documents"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    doc_name_en = Column(String(200), nullable=False)
    doc_name_ml = Column(String(200), nullable=False)
    is_mandatory = Column(Boolean, default=True)
    description_en = Column(Text, nullable=True)
    description_ml = Column(Text, nullable=True)

    service = relationship("Service", back_populates="documents")

class ServiceGuide(Base):
    __tablename__ = "service_guides"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title_en = Column(String(200), nullable=False)
    title_ml = Column(String(200), nullable=False)
    description_en = Column(Text, nullable=False)
    description_ml = Column(Text, nullable=False)
    action_url = Column(String(300), nullable=True)

    service = relationship("Service", back_populates="guides")

class ServiceFAQ(Base):
    __tablename__ = "service_faqs"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    question_en = Column(Text, nullable=False)
    question_ml = Column(Text, nullable=False)
    answer_en = Column(Text, nullable=False)
    answer_ml = Column(Text, nullable=False)

    service = relationship("Service", back_populates="faqs")
