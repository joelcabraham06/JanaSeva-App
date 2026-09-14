from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.service import ServiceDocument, Service
from app.models.admin import AdminUser, AuditLog
from app.schemas.service import DocumentCreate, DocumentResponse
from app.api.v1.endpoints.auth import get_current_admin

router = APIRouter()

@router.post("/service/{service_id}", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def add_service_document(
    service_id: int,
    doc_in: DocumentCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    doc = ServiceDocument(service_id=service_id, **doc_in.dict())
    db.add(doc)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="ADD_DOCUMENT",
        details=f"Added doc '{doc_in.doc_name_en}' to service ID {service_id}"
    )
    db.add(audit)
    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    doc = db.query(ServiceDocument).filter(ServiceDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(doc)
    audit = AuditLog(
        admin_username=current_admin.username,
        action="DELETE_DOCUMENT",
        details=f"Deleted doc ID {doc_id}"
    )
    db.add(audit)
    db.commit()
    return None
