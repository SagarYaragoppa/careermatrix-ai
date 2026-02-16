from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from app.services.recommendation_engine import recommend_careers

# 🔹 Database Imports
from app.database import engine, SessionLocal, Base
from app.models import RecommendationHistory


# ----------------------------
# Create Tables Automatically
# ----------------------------
Base.metadata.create_all(bind=engine)


# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(title="CareerMatrix AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def health_check():
    return {"status": "CareerMatrix AI Backend Running"}


# ----------------------------
# Request Model
# ----------------------------
class UserInput(BaseModel):
    skills: List[str]
    interests: List[str]
    career_mode: str
    risk_preference: str


# ----------------------------
# Recommendation Endpoint
# ----------------------------
@app.post("/recommend")
def recommend(user: UserInput):

    result = recommend_careers(user.dict())
    db = SessionLocal()

    try:
        new_record = RecommendationHistory(
            skills=", ".join(user.skills),
            interests=", ".join(user.interests),
            career_mode=user.career_mode,
            risk_preference=user.risk_preference,
            primary_career=result["primary_recommendation"]["career"],
            backup_career=result["backup_recommendation"]["career"],
            primary_score=result["primary_recommendation"]["match_score"],
            backup_score=result["backup_recommendation"]["match_score"],
        )

        db.add(new_record)
        db.commit()

    finally:
        db.close()

    return result


# ----------------------------
# Get Recommendation History
# ----------------------------
@app.get("/history")
def get_recommendation_history():

    db = SessionLocal()

    try:
        records = (
            db.query(RecommendationHistory)
            .order_by(RecommendationHistory.created_at.desc())
            .all()
        )

        history = [
            {
                "id": record.id,
                "skills": record.skills,
                "interests": record.interests,
                "career_mode": record.career_mode,
                "risk_preference": record.risk_preference,
                "primary_career": record.primary_career,
                "backup_career": record.backup_career,
                "primary_score": record.primary_score,
                "backup_score": record.backup_score,
                "created_at": record.created_at,
            }
            for record in records
        ]

        return {"history": history}

    finally:
        db.close()


# ----------------------------
# Delete Recommendation Record
# ----------------------------
@app.delete("/history/{record_id}")
def delete_history(record_id: int):

    db = SessionLocal()

    try:
        record = db.query(RecommendationHistory).filter(
            RecommendationHistory.id == record_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()

        return {"message": "Record deleted successfully"}

    finally:
        db.close()
