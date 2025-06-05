from sqlalchemy import Column, Integer, String, Text, Enum, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import BaseModel
import enum

class SkillCategory(enum.Enum):
    PROGRAMMING_LANGUAGE = "Programming Language"
    FRAMEWORK = "Framework"
    DATABASE = "Database"
    TOOL = "Tool"
    SOFT_SKILL = "Soft Skill"
    OTHER = "Other"

class Skill(BaseModel):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(SkillCategory), nullable=False)
    proficiency_level = Column(Float, nullable=False)  # 0-100 scale
    description = Column(Text)
    icon_url = Column(String(255))  # For storing skill icons/logos
    
    # Optional fields for more detail
    years_experience = Column(Float)  # Years of experience with this skill
    is_highlighted = Column(Boolean, default=False)  # For featuring important skills
    order = Column(Integer, default=0)  # For custom ordering in UI
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Skill {self.name} ({self.category})>"