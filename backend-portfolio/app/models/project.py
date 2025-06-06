from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(255))
    github_url = Column(String(255))
    live_url = Column(String(255))
    technologies = Column(String(255), nullable=False)
    order = Column(Integer, default=0)
    
    # Status fields
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


    # Relationships
    user = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project {self.title}>"