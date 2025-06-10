from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.education import Education
from app.models.user import User
from app.schemas.education import (
    EducationCreate,
    EducationResponse,
    EducationUpdate
)
from app.core.auth_manager import get_current_user
from sqlalchemy import desc

router = APIRouter()

# Public endpoint - Get education by user_id
@router.get("/user/{user_id}", response_model=List[EducationResponse])
async def get_user_education(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's education history (public endpoint)"""
    education = db.query(Education)\
        .filter(Education.user_id == user_id)\
        .order_by(desc(Education.start_date))\
        .all()
    return education

# Protected endpoints - User manages their own education
@router.get("/my-education", response_model=List[EducationResponse])
async def get_my_education(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's education history"""
    return db.query(Education)\
        .filter(Education.user_id == current_user.id)\
        .order_by(desc(Education.start_date))\
        .all()

@router.post("/", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add new education entry"""
    db_education = Education(**education.dict(), user_id=current_user.id)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

@router.put("/{education_id}", response_model=EducationResponse)
async def update_education(
    education_id: int,
    education_update: EducationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update education entry"""
    db_education = db.query(Education)\
        .filter(
            Education.id == education_id,
            Education.user_id == current_user.id
        ).first()
    
    if not db_education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education entry not found"
        )
    
    for field, value in education_update.dict(exclude_unset=True).items():
        setattr(db_education, field, value)
    
    db.commit()
    db.refresh(db_education)
    return db_education

@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete education entry"""
    db_education = db.query(Education)\
        .filter(
            Education.id == education_id,
            Education.user_id == current_user.id
        ).first()
    
    if not db_education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education entry not found"
        )
    
    db.delete(db_education)
    db.commit()
    return None