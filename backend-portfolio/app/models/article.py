from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Article(BaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    
    # Meta information
    author_id = Column(Integer, ForeignKey("users.id"))
    featured_image = Column(String(255))
    tags = Column(String(255))  # Store as comma-separated values
    
    # Status and visibility
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    
    # # Relationships
    # author = relationship("User", back_populates="articles")

    def __repr__(self):
        return f"<Article {self.title}>"