from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
from app.db.session import get_db
from app.models.article import Article
from app.models.user import User
from app.schemas.article import (
    ArticleCreate,
    ArticleResponse,
    ArticleUpdate,
    ArticleWithAuthorResponse
)
from app.core.auth_manager import get_current_user, get_current_admin
from sqlalchemy.sql import func


router = APIRouter()

# Public endpoints
@router.get("/", response_model=List[ArticleWithAuthorResponse])
async def get_articles(  
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all published articles with filtering and pagination"""
    query = db.query(Article).filter(Article.is_published == True)
    
    if search:
        query = query.filter(Article.title.ilike(f"%{search}%"))
    if category:
        query = query.filter(Article.category == category)
    if is_featured is not None:
        query = query.filter(Article.is_featured == is_featured)
    
    return query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()


# User-specific endpoints
@router.get("/my-articles", response_model=List[ArticleResponse])
async def get_my_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's articles"""
    return db.query(Article)\
        .filter(Article.author_id == current_user.id)\
        .order_by(desc(Article.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

@router.post("/new", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new article"""
    db_article = Article(**article.dict(), author_id=current_user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/{article_id}", response_model=ArticleWithAuthorResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific published article"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(  
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's article"""
    db_article = current_user.articles.filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this article"
        )

    for field, value in article_update.dict(exclude_unset=True).items():
        setattr(db_article, field, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user's article"""
    db_article = current_user.articles.filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this article"
        )
    
    db.delete(db_article)
    db.commit()
    return None

# Admin-specific endpoints
@router.put("/{article_id}/publish", response_model=ArticleResponse)
async def toggle_article_publish(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle article published status (admin only)"""
    db_article = current_user.articles.filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    db_article.is_published = not db_article.is_published
    if db_article.is_published:
        db_article.published_at = func.now()
    
    db.commit()
    db.refresh(db_article)
    return db_article

@router.put("/{article_id}/feature", response_model=ArticleResponse)
async def toggle_article_feature(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle article featured status (admin only)"""
    db_article = current_user.articles.filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    db_article.is_featured = not db_article.is_featured
    db.commit()
    db.refresh(db_article)
    return db_article