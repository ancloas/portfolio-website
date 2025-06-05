from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import router as api_router
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.logger import logger
from app.db.session import engine
from app.models import Base  # Import Base from models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"Starting application: {settings.PROJECT_NAME} v{settings.API_V1_STR}")
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    yield  # Application runs here
    
    # Shutdown logic
    logger.info("Shutting down application...")

app = FastAPI(
    title="Portfolio API",
    description="Backend API for Portfolio Website",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")