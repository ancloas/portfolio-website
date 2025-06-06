from sqlalchemy import Column, Integer, String, Text, Enum, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
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
    name = Column(String(100), nullable=False, unique=True)
    category = Column(Enum(SkillCategory), nullable=False)
    icon_url = Column(String(255))  # For storing skill icons/logos
    description = Column(Text)  # General description of the skill
    is_active = Column(Boolean, default=True)  # To soft delete skills
    
    # Relationships
    users = relationship("SkillUser", back_populates="skill")

    def __repr__(self):
        return f"<Skill {self.name} ({self.category})>"

class SkillUser(BaseModel):
    __tablename__ = "skill_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    
    # Skill details
    proficiency_level = Column(Float, nullable=False)  # User-specific proficiency level
    years_experience = Column(Float)  # Years of experience with this skill
    description = Column(Text)  # User-specific description/notes
    is_highlighted = Column(Boolean, default=False)  # For featuring important skills
    order = Column(Integer, default=0)  # For custom ordering in UI
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    skill = relationship("Skill", back_populates="users")
    user = relationship("User", back_populates="skills")

    # Unique constraint to prevent duplicate skill-user combinations
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_id', name='unique_user_skill'),
    )

    def __repr__(self):
        return f"<SkillUser user_id={self.user_id} skill_id={self.skill_id}>"