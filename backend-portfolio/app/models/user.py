from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.models.base import BaseModel



class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)