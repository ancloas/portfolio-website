from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.skills import SkillCategory

class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    description: Optional[str] = None
    icon_url: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: Optional[str] = None
    category: Optional[SkillCategory] = None

class SkillResponse(SkillBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: float = Field(..., ge=0, le=10)
    years_experience: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    is_highlighted: Optional[bool] = False
    order: Optional[int] = 0

class UserSkillCreate(UserSkillBase):
    pass

class UserSkillUpdate(BaseModel):
    proficiency_level: Optional[float] = Field(None, ge=0, le=10)
    years_experience: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    is_highlighted: Optional[bool] = None
    order: Optional[int] = None

class UserSkillResponse(UserSkillBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    skill: SkillResponse

    class Config:
        from_attributes = True