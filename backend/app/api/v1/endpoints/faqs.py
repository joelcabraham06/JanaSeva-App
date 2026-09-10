from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.service import ServiceFAQ, Service
from app.models.admin import AdminUser, AuditLog
from app.schemas.service import FAQCreate, FAQResponse
from app.api.v1.endpoints.auth import get_current_admin

router = APIRouter()

@router.post("/service/{service_id}", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def add_service_faq(
    service_id: int,
    faq_in: FAQCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    faq = ServiceFAQ(service_id=service_id, **faq_in.dict())
    db.add(faq)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="ADD_FAQ",
        details=f"Added FAQ to service ID {service_id}"
    )
    db.add(audit)
    db.commit()
    db.refresh(faq)
    return faq

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    faq = db.query(ServiceFAQ).filter(ServiceFAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    db.delete(faq)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="DELETE_FAQ",
        details=f"Deleted FAQ ID {faq_id}"
    )
    db.add(audit)
    db.commit()
    return None
