import pytest
import os
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

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_admin_login():
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "testadmin", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_admin_login_invalid_password():
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "testadmin", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_admin_me_endpoint():
    login_res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "testadmin", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    me_res = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "testadmin"
