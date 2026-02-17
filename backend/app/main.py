from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.services.jwt_dependency import get_current_user

import shutil
import os

from app.services.recommendation_engine import recommend_careers
from app.services.resume_parser.resume_service import process_resume

# Database
from app.database import engine, SessionLocal, Base
from app.models import RecommendationHistory, User
from app.services.auth_service import hash_password, verify_password, create_access_token


# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(title="CareerMatrix AI")


# ----------------------------
# Middleware
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Create Tables
# ----------------------------
Base.metadata.create_all(bind=engine)


# ----------------------------
# Upload Folder
# ----------------------------
UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------------------
# Request Models
# ----------------------------

class UserInput(BaseModel):
    skills: List[str]
    interests: List[str]
    career_mode: str
    risk_preference: str


class AuthRequest(BaseModel):
    email: str
    password: str


# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def health_check():
    return {"status": "CareerMatrix AI Backend Running"}


# ----------------------------
# Signup
# ----------------------------
@app.post("/signup")
def signup(user: AuthRequest):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {"message": "User created successfully"}


# ----------------------------
# Login
# ----------------------------
@app.post("/login")
def login(user: AuthRequest):
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ----------------------------
# Resume Upload
# ----------------------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed_data = process_resume(file_path)

    return parsed_data


# ----------------------------
# Upload + Recommend
# ----------------------------
# ----------------------------
# Upload + Recommend
# ----------------------------
@app.post("/upload-and-recommend")
async def upload_and_recommend(
    file: UploadFile = File(...),
    career_mode: str = "growth",
    risk_preference: str = "medium",
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Parse resume
    parsed_data = process_resume(file_path)

    # 3️⃣ Prepare recommendation input
    user_input = {
        "skills": parsed_data.get("skills", []),
        "interests": [],
        "career_mode": career_mode,
        "risk_preference": risk_preference
    }

    # 4️⃣ Generate recommendation
    result = recommend_careers(user_input)

    # 5️⃣ Save to database
    db = SessionLocal()
    try:
        new_record = RecommendationHistory(
            user_id=current_user.id,
            skills=", ".join(parsed_data.get("skills", [])),
            interests="",
            career_mode=career_mode,
            risk_preference=risk_preference,
            primary_career=result["primary_recommendation"]["career"],
            backup_career=result["backup_recommendation"]["career"],
            primary_score=result["primary_recommendation"]["match_score"],
            backup_score=result["backup_recommendation"]["match_score"],
        )

        db.add(new_record)
        db.commit()

    finally:
        db.close()

    # 6️⃣ Return response
    return {
        "resume_data": parsed_data,
        "recommendation": result
    }


# ----------------------------
# Recommend (Manual Form)
# ----------------------------
@app.post("/recommend")
def recommend(
    user: UserInput,
    current_user: User = Depends(get_current_user)
):


    result = recommend_careers(user.dict())
    db = SessionLocal()

    try:
        new_record = RecommendationHistory(
            user_id=current_user.id,
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
# History
# ----------------------------
@app.get("/history")
def get_recommendation_history(
    current_user: User = Depends(get_current_user)
):


    db = SessionLocal()

    try:
        records = (
            db.query(RecommendationHistory)
            .filter(RecommendationHistory.user_id == current_user.id)
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
# Delete History
# ----------------------------
@app.delete("/history/{record_id}")
def delete_history(
    record_id: int,
    current_user: User = Depends(get_current_user)
):


    db = SessionLocal()

    try:
        record = db.query(RecommendationHistory).filter(
            RecommendationHistory.id == record_id,
            RecommendationHistory.user_id == current_user.id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()

        return {"message": "Record deleted successfully"}

    finally:
        db.close()
