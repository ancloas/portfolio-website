from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.skills import Skill, SkillUser, SkillCategory
from app.models.user import User
from app.schemas.skill import (
    SkillCreate, 
    SkillResponse, 
    SkillUpdate,
    UserSkillCreate,
    UserSkillResponse,
    UserSkillUpdate
)
from app.core.auth_manager import get_current_user, get_current_admin
from sqlalchemy import desc

router = APIRouter()

# Skills endpoints (general skills management)
@router.get("/", response_model=List[SkillResponse])
async def get_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[SkillCategory] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available skills"""
    query = db.query(Skill).filter(Skill.is_active == True)
    
    if category:
        query = query.filter(Skill.category == category)
    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))
    
    return query.order_by(Skill.name).offset(skip).limit(limit).all()

# User-specific skill endpoints
@router.get("/my-skills", response_model=List[UserSkillResponse])
async def get_my_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's skills"""
    return db.query(SkillUser).filter(
        SkillUser.user_id == current_user.id,
        SkillUser.is_active == True
    ).order_by(SkillUser.order).offset(skip).limit(limit).all()

@router.post("/add-skill", response_model=UserSkillResponse)
async def add_user_skill(
    skill: UserSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a skill to current user's profile"""
    # Check if skill exists
    db_skill = db.query(Skill).filter(Skill.id == skill.skill_id).first()
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    # Check if user already has this skill
    existing_skill = db.query(SkillUser).filter(
        SkillUser.user_id == current_user.id,
        SkillUser.skill_id == skill.skill_id
    ).first()
    
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already added to user profile"
        )
    
    # Create new user skill
    db_user_skill = SkillUser(
        user_id=current_user.id,
        **skill.dict()
    )
    db.add(db_user_skill)
    db.commit()
    db.refresh(db_user_skill)
    return db_user_skill

@router.put("/my-skills/{skill_id}", response_model=UserSkillResponse)
async def update_user_skill(
    skill_id: int,
    skill_update: UserSkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's skill details"""
    db_user_skill = db.query(SkillUser).filter(
        SkillUser.skill_id == skill_id,
        SkillUser.user_id == current_user.id
    ).first()
    
    if not db_user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found in your profile"
        )
    
    for field, value in skill_update.dict(exclude_unset=True).items():
        setattr(db_user_skill, field, value)
    
    db.commit()
    db.refresh(db_user_skill)
    return db_user_skill

@router.delete("/my-skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a skill from user's profile"""
    db_user_skill = db.query(SkillUser).filter(
        SkillUser.skill_id == skill_id,
        SkillUser.user_id == current_user.id
    ).first()
    
    if not db_user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found in your profile"
        )
    
    db.delete(db_user_skill)
    db.commit()
    return None

@router.put("/my-skills/{skill_id}/highlight")
async def toggle_skill_highlight(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle highlight status of a user's skill"""
    db_user_skill = db.query(SkillUser).filter(
        SkillUser.skill_id == skill_id,
        SkillUser.user_id == current_user.id
    ).first()
    
    if not db_user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found in your profile"
        )
    
    db_user_skill.is_highlighted = not db_user_skill.is_highlighted
    db.commit()
    return {"message": f"Skill highlight status set to {db_user_skill.is_highlighted}"}




# Admin-only skill management endpoints
@router.post("/admin/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # Ensure admin access
):
    """Create a new skill (admin only)"""
    # Check if skill with same name exists
    existing_skill = db.query(Skill).filter(Skill.name == skill.name).first()
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill with this name already exists"
        )
    
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.put("/admin/skills/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # Ensure admin access
):
    """Update an existing skill (admin only)"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    # Check name uniqueness if name is being updated
    if skill_update.name and skill_update.name != db_skill.name:
        existing_skill = db.query(Skill).filter(Skill.name == skill_update.name).first()
        if existing_skill:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill with this name already exists"
            )
    
    for field, value in skill_update.dict(exclude_unset=True).items():
        setattr(db_skill, field, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/admin/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # Ensure admin access
):
    """Delete a skill (admin only)"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    # Check if skill is being used by any users
    skill_users = db.query(SkillUser).filter(SkillUser.skill_id == skill_id).first()
    if skill_users:
        # Soft delete instead of hard delete if skill is in use
        db_skill.is_active = False
        db.commit()
        return None
    
    # Hard delete if skill is not in use
    db.delete(db_skill)
    db.commit()
    return None

@router.put("/admin/skills/{skill_id}/restore", response_model=SkillResponse)
async def restore_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # Ensure admin access
):
    """Restore a soft-deleted skill (admin only)"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    db_skill.is_active = True
    db.commit()
    db.refresh(db_skill)
    return db_skill