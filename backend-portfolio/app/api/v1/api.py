from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth_manager import auth_handler, get_current_user, get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.api.v1.endpoints import projects, auth, articles, skills, education

router = APIRouter()

@router.post("/")
async def test():
    return 'Working'

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api": "v1"
    }


# @router.get("/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# @router.get("/admin-only")
# async def admin_only(current_user: User = Depends(get_current_admin)):
#     return {"message": "Hello admin!"}


router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)


router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)



router.include_router(
    articles.router,
    prefix="/articles",
    tags=["articles"]
)



router.include_router(
    skills.router,
    prefix="/skills",
    tags=["skills"]
)



router.include_router(
    education.router,
    prefix="/education",
    tags=["education"]
)



