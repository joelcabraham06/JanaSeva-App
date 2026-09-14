from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.service import Service, ServiceDocument, ServiceGuide, ServiceFAQ
from app.models.admin import AdminUser, AuditLog
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.api.v1.endpoints.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
def get_services(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Service).filter(Service.is_active == True)
    if category:
        query = query.filter(Service.category == category)
    return query.offset(skip).limit(limit).all()

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    existing = db.query(Service).filter(Service.slug == service_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Service slug already exists")

    service = Service(
        slug=service_in.slug,
        category=service_in.category,
        name_en=service_in.name_en,
        name_ml=service_in.name_ml,
        description_en=service_in.description_en,
        description_ml=service_in.description_ml,
        eligibility_en=service_in.eligibility_en,
        eligibility_ml=service_in.eligibility_ml,
        application_fee=service_in.application_fee,
        processing_time_days=service_in.processing_time_days,
        online_available=service_in.online_available,
        offline_available=service_in.offline_available,
        official_website=service_in.official_website,
        office_type=service_in.office_type,
        source_url=service_in.source_url,
        aliases_en=service_in.aliases_en,
        aliases_ml=service_in.aliases_ml,
        aliases_manglish=service_in.aliases_manglish
    )
    db.add(service)
    db.flush()

    # Add embedded nested documents
    if service_in.documents:
        for doc in service_in.documents:
            db.add(ServiceDocument(service_id=service.id, **doc.dict()))

    # Add embedded nested guides
    if service_in.guides:
        for guide in service_in.guides:
            db.add(ServiceGuide(service_id=service.id, **guide.dict()))

    # Add embedded nested faqs
    if service_in.faqs:
        for faq in service_in.faqs:
            db.add(ServiceFAQ(service_id=service.id, **faq.dict()))

    # Audit log
    audit = AuditLog(
        admin_username=current_admin.username,
        action="CREATE_SERVICE",
        details=f"Created service: {service.name_en} ({service.slug})"
    )
    db.add(audit)
    db.commit()
    db.refresh(service)
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = service_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)

    audit = AuditLog(
        admin_username=current_admin.username,
        action="UPDATE_SERVICE",
        details=f"Updated service ID {service_id}: {list(update_data.keys())}"
    )
    db.add(audit)
    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.is_active = False  # Soft delete
    audit = AuditLog(
        admin_username=current_admin.username,
        action="DELETE_SERVICE",
        details=f"Deactivated service ID {service_id}"
    )
    db.add(audit)
    db.commit()
    return None
