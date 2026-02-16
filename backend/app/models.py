from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id = Column(Integer, primary_key=True, index=True)

    skills = Column(Text)
    interests = Column(Text)
    career_mode = Column(String)
    risk_preference = Column(String)

    primary_career = Column(String)
    backup_career = Column(String)

    primary_score = Column(Float)
    backup_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
