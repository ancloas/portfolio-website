from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceInDBBase,
    ExperienceUpdate
)
from app.core.auth_manager import get_current_user
from sqlalchemy import desc

router = APIRouter()

# Public endpoint - Get experiences by user_id
@router.get("/user/{user_id}", response_model=List[ExperienceResponse])
async def get_user_experiences(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's experience history (public endpoint)"""
    experiences = db.query(Experience)\
        .filter(Experience.user_id == user_id)\
        .order_by(desc(Experience.start_date))\
        .all()
    return experiences

# Protected endpoints - User manages their own experiences
@router.get("/my-experiences", response_model=List[ExperienceInDBBase])
async def get_my_experiences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's experience history"""
    return db.query(Experience)\
        .filter(Experience.user_id == current_user.id)\
        .order_by(desc(Experience.start_date))\
        .all()

@router.post("/create", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add new experience entry"""
    db_experience = Experience(**experience.dict(), user_id=current_user.id)
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update experience entry"""
    db_experience = db.query(Experience)\
        .filter(
            Experience.id == experience_id,
            Experience.user_id == current_user.id
        ).first()
    
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience entry not found"
        )
    
    for field, value in experience_update.dict(exclude_unset=True).items():
        if value:
            setattr(db_experience, field, value)
    
    db.commit()
    db.refresh(db_experience)
    return db_experience

@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete experience entry"""
    db_experience = db.query(Experience)\
        .filter(
            Experience.id == experience_id,
            Experience.user_id == current_user.id
        ).first()
    
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience entry not found"
        )
    
    db.delete(db_experience)
    db.commit()
    return None