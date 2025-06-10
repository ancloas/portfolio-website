from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Education(BaseModel):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    field_of_study = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    description = Column(Text)
    location = Column(String(255))
    grade = Column(String(50))
    achievements = Column(Text)
    insitution_icon_url = Column(String(255))

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="education")