# recommendation_engine.py

from typing import List, Dict


# ----------------------------
# Sample Career Dataset
# ----------------------------

CAREER_DATABASE = [
    {
        "name": "Machine Learning Engineer",
        "required_skills": ["python", "math", "machine learning"],
        "growth_score": 9,
        "stability_score": 7,
        "market_demand": 8,
        "domain": "tech",
    },
    {
        "name": "Data Analyst",
        "required_skills": ["python", "sql", "statistics"],
        "growth_score": 7,
        "stability_score": 8,
        "market_demand": 8,
        "domain": "tech",
    },
    {
        "name": "Software Developer",
        "required_skills": ["programming", "problem solving"],
        "growth_score": 8,
        "stability_score": 8,
        "market_demand": 9,
        "domain": "tech",
    },
    {
        "name": "Investment Banker",
        "required_skills": ["finance", "communication", "analysis"],
        "growth_score": 9,
        "stability_score": 6,
        "market_demand": 7,
        "domain": "finance",
    },
    {
        "name": "Government Officer",
        "required_skills": ["general knowledge", "administration"],
        "growth_score": 6,
        "stability_score": 10,
        "market_demand": 6,
        "domain": "public",
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


def score_career(user_input: Dict, career: Dict) -> float:
    """
    Generates weighted score for a single career
    """

    skill_score = calculate_skill_match(user_input["skills"], career["required_skills"])

    # Base score from skills (40%)
    total_score = skill_score * 40

    # Growth or stability preference (30%)
    if user_input["career_mode"] == "growth":
        total_score += career["growth_score"] * 3
    else:
        total_score += career["stability_score"] * 3

    # Market demand weight (30%)
    total_score += career["market_demand"] * 3

    return total_score


def analyze_career(user_input: Dict, career: Dict) -> Dict:
    """
    Returns detailed analysis for a career
    """

    user_skills = set(user_input["skills"])
    career_skills = set(career["required_skills"])

    matched_skills = list(user_skills.intersection(career_skills))
    missing_skills = list(career_skills.difference(user_skills))

    score = score_career(user_input, career)

    return {
        "career": career["name"],
        "match_score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "growth_score": career["growth_score"],
        "stability_score": career["stability_score"],
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
        "skills": ["python", "math", "machine learning"],
        "career_mode": "growth"
    }

    result = recommend_careers(user)
    print(result)
