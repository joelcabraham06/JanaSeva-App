import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine, Base, SessionLocal
from app.models.admin import AdminUser
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("janaseva")

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Multilingual WhatsApp-based Government Service Assistant API",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """
    On startup, ensure initial admin account exists in database.
    """
    db: Session = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == settings.FIRST_ADMIN_USERNAME).first()
        if not admin:
            hashed_pwd = get_password_hash(settings.FIRST_ADMIN_PASSWORD)
            first_admin = AdminUser(
                username=settings.FIRST_ADMIN_USERNAME,
                password_hash=hashed_pwd,
                email="admin@janaseva.gov.in",
                role="SUPERADMIN"
            )
            db.add(first_admin)
            db.commit()
            logger.info(f"Created default admin user: '{settings.FIRST_ADMIN_USERNAME}'")
    except Exception as e:
        logger.error(f"Startup DB init error: {e}")
    finally:
        db.close()

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "Janaseva Backend API", "version": "1.0.0"}

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to Janaseva Multilingual Government Assistant API",
        "documentation": "/docs",
        "health": "/health"
    }
