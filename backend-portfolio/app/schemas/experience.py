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

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(ExperienceBase):
    pass

class ExperienceInDBBase(ExperienceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Experience(ExperienceInDBBase):
    pass