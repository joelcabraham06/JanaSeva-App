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

def test_webhook_verification():
    res = client.get(
        f"{settings.API_V1_STR}/webhook/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": settings.WHATSAPP_VERIFY_TOKEN,
            "hub.challenge": "12345678"
        }
    )
    assert res.status_code == 200
    assert res.text == "12345678"

def test_simulator_first_message_triggers_language_prompt():
    res = client.post(
        f"{settings.API_V1_STR}/webhook/simulator",
        json={"phone_number": "919999999999", "text_body": "hi"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "Janaseva" in data["reply_text"]
    assert len(data["interactive_buttons"]) == 2

def test_simulator_select_language_and_search():
    # Select Malayalam
    lang_res = client.post(
        f"{settings.API_V1_STR}/webhook/simulator",
        json={"phone_number": "919888888888", "text_body": "lang_ml"}
    )
    assert lang_res.status_code == 200

    # Search DL Renewal
    search_res = client.post(
        f"{settings.API_V1_STR}/webhook/simulator",
        json={"phone_number": "919888888888", "text_body": "license puthukkanam"}
    )
    assert search_res.status_code == 200
    assert "ഡ്രൈവിംഗ്" in search_res.json()["reply_text"] or "Licence" in search_res.json()["reply_text"]
