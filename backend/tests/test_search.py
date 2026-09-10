import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base, AdminUser, Service, User
from app.db.session import get_db
from app.core.config import settings
from seed_data import seed_database

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
    seed_database(db)
    db.close()
    yield

client = TestClient(app)

def test_search_manglish_license():
    res = client.post(
        f"{settings.API_V1_STR}/search/query",
        json={"query": "license puthukkanam"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["detected_language"] == "manglish"
    assert len(data["matched_services"]) > 0

def test_search_malayalam_passport():
    res = client.post(
        f"{settings.API_V1_STR}/search/query",
        json={"query": "പാസ്പോർട്ട് അപേക്ഷ"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["detected_language"] == "ml"
    assert len(data["matched_services"]) > 0

def test_search_english_aadhaar():
    res = client.post(
        f"{settings.API_V1_STR}/search/query",
        json={"query": "aadhaar update"}
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data["matched_services"]) > 0
