from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.service import ServiceGuide, Service
from app.models.admin import AdminUser, AuditLog
from app.schemas.service import GuideCreate, GuideResponse
from app.api.v1.endpoints.auth import get_current_admin

router = APIRouter()

@router.post("/service/{service_id}", response_model=GuideResponse, status_code=status.HTTP_201_CREATED)
def add_service_guide_step(
    service_id: int,
    guide_in: GuideCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    guide = ServiceGuide(service_id=service_id, **guide_in.dict())
    db.add(guide)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="ADD_GUIDE_STEP",
        details=f"Added Step {guide_in.step_number} to service ID {service_id}"
    )
    db.add(audit)
    db.commit()
    db.refresh(guide)
    return guide

@router.delete("/{guide_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_guide_step(
    guide_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    guide = db.query(ServiceGuide).filter(ServiceGuide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide step not found")

    db.delete(guide)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="DELETE_GUIDE_STEP",
        details=f"Deleted guide step ID {guide_id}"
    )
    db.add(audit)
    db.commit()
    return None
