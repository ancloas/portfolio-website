from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.user import UserBase

class ArticleBase(BaseModel):
    title: str
    slug: str
    content: Dict
    summary: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    featured_image: Optional[HttpUrl] = None
    cover_image: Optional[HttpUrl] = None
    thumbnail: Optional[HttpUrl] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict] = None
    summary: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    featured_image: Optional[HttpUrl] = None
    cover_image: Optional[HttpUrl] = None
    thumbnail: Optional[HttpUrl] = None

class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    is_published: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime]
    published_at: Optional[datetime]
    view_count: int
    like_count: int

    class Config:
        from_attributes = True

class ArticleWithAuthorResponse(ArticleResponse):
    author: UserBase  # Basic author information

    class Config:
        from_attributes = True