from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class DocumentBase(BaseModel):
    doc_name_en: str
    doc_name_ml: str
    is_mandatory: bool = True
    description_en: Optional[str] = None
    description_ml: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    service_id: int

    class Config:
        from_attributes = True

class GuideBase(BaseModel):
    step_number: int
    title_en: str
    title_ml: str
    description_en: str
    description_ml: str
    action_url: Optional[str] = None

class GuideCreate(GuideBase):
    pass

class GuideResponse(GuideBase):
    id: int
    service_id: int

    class Config:
        from_attributes = True

class FAQBase(BaseModel):
    question_en: str
    question_ml: str
    answer_en: str
    answer_ml: str

class FAQCreate(FAQBase):
    pass

class FAQResponse(FAQBase):
    id: int
    service_id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    slug: str
    category: str
    name_en: str
    name_ml: str
    description_en: str
    description_ml: str
    eligibility_en: Optional[str] = None
    eligibility_ml: Optional[str] = None
    application_fee: str = "Free / Standard Fee"
    processing_time_days: Optional[int] = 7
    online_available: bool = True
    offline_available: bool = True
    official_website: str
    office_type: str = "Akshaya Center / RTO / Panchayat"
    source_url: Optional[str] = None
    aliases_en: Optional[str] = None
    aliases_ml: Optional[str] = None
    aliases_manglish: Optional[str] = None

class ServiceCreate(ServiceBase):
    documents: Optional[List[DocumentCreate]] = []
    guides: Optional[List[GuideCreate]] = []
    faqs: Optional[List[FAQCreate]] = []

class ServiceUpdate(BaseModel):
    category: Optional[str] = None
    name_en: Optional[str] = None
    name_ml: Optional[str] = None
    description_en: Optional[str] = None
    description_ml: Optional[str] = None
    eligibility_en: Optional[str] = None
    eligibility_ml: Optional[str] = None
    application_fee: Optional[str] = None
    processing_time_days: Optional[int] = None
    online_available: Optional[bool] = None
    offline_available: Optional[bool] = None
    official_website: Optional[str] = None
    office_type: Optional[str] = None
    source_url: Optional[str] = None
    aliases_en: Optional[str] = None
    aliases_ml: Optional[str] = None
    aliases_manglish: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    is_active: bool
    last_updated: datetime
    documents: List[DocumentResponse] = []
    guides: List[GuideResponse] = []
    faqs: List[FAQResponse] = []

    class Config:
        from_attributes = True
