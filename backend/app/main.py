from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.services.recommendation_engine import recommend_careers


app = FastAPI(title="CareerMatrix AI")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "CareerMatrix AI Backend Running"}


# ----------------------------
# Request Model (Input Schema)
# ----------------------------

class UserInput(BaseModel):
    skills: List[str]
    interests: List[str]
    career_mode: str   # "growth" or "stability"
    risk_preference: str  # "low" / "medium" / "high"


# ----------------------------
# API Endpoint
# ----------------------------

@app.post("/recommend")
def recommend(user_input: UserInput):
    result = recommend_careers(user_input.dict())
    return result
