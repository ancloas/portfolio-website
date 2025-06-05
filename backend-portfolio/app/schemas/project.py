from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    """Base schema for Project with common attributes"""
    title: str
    description: str
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    technologies: str
    order: Optional[int] = None

class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    pass

class ProjectUpdate(ProjectBase):
    """Schema for updating a project"""
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None

class ProjectResponse(ProjectBase):
    """Schema for project responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Configure Pydantic to parse ORM objects"""
        from_attributes = True