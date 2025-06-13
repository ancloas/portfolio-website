from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExperienceBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class ExperienceResponse(ExperienceBase):
    pass
class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


 
class ExperienceInDBBase(ExperienceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Experience(ExperienceInDBBase):
    pass