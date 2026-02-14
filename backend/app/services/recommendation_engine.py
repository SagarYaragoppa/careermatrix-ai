# recommendation_engine.py

from typing import List, Dict


# ----------------------------
# Sample Career Dataset
# ----------------------------

CAREER_DATABASE = [
    {
        "name": "Machine Learning Engineer",
        "required_skills": ["python", "math", "machine learning"],
        "related_interests": ["ai", "technology", "research"],
        "growth_score": 9,
        "stability_score": 7,
        "market_demand": 8,
        "risk_level": 6
    },
    {
        "name": "Data Analyst",
        "required_skills": ["python", "sql", "statistics"],
        "related_interests": ["data", "analysis", "business"],
        "growth_score": 7,
        "stability_score": 8,
        "market_demand": 8,
        "risk_level": 4
    },
    {
        "name": "Investment Banker",
        "required_skills": ["finance", "communication", "analysis"],
        "related_interests": ["finance", "markets", "business"],
        "growth_score": 9,
        "stability_score": 6,
        "market_demand": 7,
        "risk_level": 8
    },
    {
        "name": "Government Officer",
        "required_skills": ["general knowledge", "administration"],
        "related_interests": ["public service", "administration"],
        "growth_score": 6,
        "stability_score": 10,
        "market_demand": 6,
        "risk_level": 2
    },
]


# ----------------------------
# Scoring Logic
# ----------------------------


def calculate_skill_match(user_skills: List[str], career_skills: List[str]) -> float:
    """
    Calculates percentage overlap between user skills and required skills
    """
    matches = set(user_skills).intersection(set(career_skills))
    return len(matches) / len(career_skills)

def calculate_interest_match(user_interests: List[str], career_interests: List[str]) -> float:
    matches = set(user_interests).intersection(set(career_interests))
    return len(matches) / len(career_interests)

def score_career(user_input: Dict, career: Dict) -> Dict:

    breakdown = {}

    # ---------------- Skill Score (35%)
    skill_score_raw = calculate_skill_match(
        user_input["skills"],
        career["required_skills"]
    )
    skill_score = skill_score_raw * 35
    breakdown["skill_score"] = round(skill_score, 2)

    # ---------------- Interest Score (20%)
    interest_score_raw = calculate_interest_match(
        user_input["interests"],
        career["related_interests"]
    )
    interest_score = interest_score_raw * 20
    breakdown["interest_score"] = round(interest_score, 2)

    # ---------------- Growth/Stability (25%)
    if user_input["career_mode"] == "growth":
        pref_score = career["growth_score"] * 2.5
        breakdown["mode_type"] = "growth"
    else:
        pref_score = career["stability_score"] * 2.5
        breakdown["mode_type"] = "stability"

    breakdown["growth_or_stability_score"] = round(pref_score, 2)

    # ---------------- Market Demand (20%)
    market_score = career["market_demand"] * 2
    breakdown["market_score"] = round(market_score, 2)

    # ---------------- Risk Alignment
    user_risk = user_input["risk_preference"]

    if user_risk == "low":
        risk_alignment = 10 - abs(career["risk_level"] - 2)
    elif user_risk == "medium":
        risk_alignment = 10 - abs(career["risk_level"] - 5)
    else:
        risk_alignment = 10 - abs(career["risk_level"] - 8)

    breakdown["risk_alignment_score"] = round(risk_alignment, 2)

    # ---------------- Total Score
    total_score = (
        skill_score +
        interest_score +
        pref_score +
        market_score +
        risk_alignment
    )

    breakdown["total_score"] = round(total_score, 2)

    return breakdown

    # Skill Match (35%)
    skill_score = calculate_skill_match(
        user_input["skills"],
        career["required_skills"]
    )
    total_score = skill_score * 35

    # Interest Match (20%)
    interest_score = calculate_interest_match(
        user_input["interests"],
        career["related_interests"]
    )
    total_score += interest_score * 20

    # Growth or Stability Preference (25%)
    if user_input["career_mode"] == "growth":
        total_score += career["growth_score"] * 2.5
    else:
        total_score += career["stability_score"] * 2.5

    # Market Demand (20%)
    total_score += career["market_demand"] * 2

    # Risk Preference Adjustment
    user_risk = user_input["risk_preference"]

    if user_risk == "low":
        risk_alignment = 10 - abs(career["risk_level"] - 2)
    elif user_risk == "medium":
        risk_alignment = 10 - abs(career["risk_level"] - 5)
    else:  # high
        risk_alignment = 10 - abs(career["risk_level"] - 8)

    total_score += risk_alignment

    return total_score



def analyze_career(user_input: Dict, career: Dict) -> Dict:

    user_skills = set(user_input["skills"])
    career_skills = set(career["required_skills"])

    matched_skills = list(user_skills.intersection(career_skills))
    missing_skills = list(career_skills.difference(user_skills))

    score_data = score_career(user_input, career)

    return {
        "career": career["name"],
        "match_score": score_data["total_score"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_breakdown": score_data,
        "risk_level": career["risk_level"],
        "market_demand": career["market_demand"]
    }


def recommend_careers(user_input: Dict) -> Dict:

    analyzed_results = []

    for career in CAREER_DATABASE:
        analysis = analyze_career(user_input, career)
        analyzed_results.append(analysis)

    # Sort by match score
    analyzed_results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "primary_recommendation": analyzed_results[0],
        "backup_recommendation": analyzed_results[1]
    }



if __name__ == "__main__":
    user = {
        "skills": ["python", "math"],
        "interests": ["ai", "technology"],
        "career_mode": "growth",
        "risk_preference": "high"
    }

    result = recommend_careers(user)
    print(result)

