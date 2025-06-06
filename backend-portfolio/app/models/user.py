from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(100))
    password_hash = Column(String(255))
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    articles = relationship("Article", 
                          back_populates="author",
                          cascade="all, delete-orphan",
                          lazy="dynamic")
    
    projects = relationship("Project", 
                          back_populates="user",
                          cascade="all, delete-orphan",
                          lazy="dynamic")
    
    skills = relationship("SkillUser", 
                         back_populates="user",
                         cascade="all, delete-orphan",
                         lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"