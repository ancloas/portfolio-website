from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import date

class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    achievements: Optional[str] = None
    insitution_icon_url: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    achievements: Optional[str] = None
    insitution_icon_url: Optional[str] = None

class EducationResponse(EducationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True