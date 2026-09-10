import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base, AdminUser, Service, User
from app.db.session import get_db
from app.core.config import settings
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_janaseva_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    if not db.query(AdminUser).filter(AdminUser.username == "testadmin").first():
        db.add(AdminUser(username="testadmin", password_hash=get_password_hash("password123"), role="SUPERADMIN"))
        db.commit()
    db.close()
    yield

client = TestClient(app)

def get_auth_token():
    res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "testadmin", "password": "password123"}
    )
    return res.json()["access_token"]

def test_create_and_get_service():
    token = get_auth_token()
    unique_slug = f"test-service-{uuid.uuid4().hex[:6]}"
    payload = {
        "slug": unique_slug,
        "category": "Test Category",
        "name_en": "Test Service EN",
        "name_ml": "ടെസ്റ്റ് സേവനം",
        "description_en": "Test Description EN",
        "description_ml": "ടെസ്റ്റ് വിവരണം",
        "application_fee": "₹100",
        "official_website": "https://test.gov.in",
        "office_type": "Akshaya",
        "documents": [
            {"doc_name_en": "Aadhaar Card", "doc_name_ml": "ആധാർ കാർഡ്", "is_mandatory": True}
        ]
    }
    create_res = client.post(
        f"{settings.API_V1_STR}/services/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["slug"] == unique_slug
    assert len(data["documents"]) == 1

    get_res = client.get(f"{settings.API_V1_STR}/services/{data['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["name_en"] == "Test Service EN"
