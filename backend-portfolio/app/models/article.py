from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from typing import List, Optional
import json

class Article(BaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    content = Column(JSON, nullable=False)  # Store rich text content as JSON
    summary = Column(String(500))
    
    # Meta information
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    featured_image = Column(String(255))
    meta_description = Column(String(160))  # For SEO
    meta_keywords = Column(String(255))  # For SEO
    
    # Rich media and formatting
    cover_image = Column(String(255))  # Hero image
    thumbnail = Column(String(255))  # Thumbnail for listings
    reading_time = Column(Integer)  # Estimated reading time in minutes
    
    # Categories and tags
    category = Column(String(100))
    tags = Column(JSON)  # Store tags as JSON array
    
    # Content structure
    content_blocks = Column(JSON)  # Store structured content blocks
    
    # Status and visibility
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    allow_comments = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    
    # Analytics
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # Relationships
    author = relationship("User", 
                         back_populates="articles",
                         lazy="joined")  # Eager loading for author

    # Helper properties and methods
    @property
    def formatted_tags(self) -> List[str]:
        """Convert JSON tags to list"""
        return json.loads(self.tags) if self.tags else []

    @property
    def structured_content(self) -> dict:
        """Get structured content blocks"""
        return json.loads(self.content_blocks) if self.content_blocks else {}

    def update_content(self, content_data: dict):
        """Update rich text content"""
        self.content = json.dumps(content_data)

    def add_tag(self, tag: str):
        """Add a new tag"""
        current_tags = self.formatted_tags
        if tag not in current_tags:
            current_tags.append(tag)
            self.tags = json.dumps(current_tags)

    def remove_tag(self, tag: str):
        """Remove a tag"""
        current_tags = self.formatted_tags
        if tag in current_tags:
            current_tags.remove(tag)
            self.tags = json.dumps(current_tags)

    def __repr__(self):
        return f"<Article {self.title}>"