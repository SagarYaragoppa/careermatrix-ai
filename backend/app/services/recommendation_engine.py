# recommendation_engine.py

from typing import List, Dict
from app.services.career_database import CAREER_DATABASE







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
    """
    Performs full career analysis including:
    - Skill match
    - Missing skills
    - Explainable score breakdown
    - Skill gap learning plan
    - 6–12 month roadmap
    """

    user_skills = set(user_input["skills"])
    career_skills = set(career["required_skills"])

    matched_skills = list(user_skills.intersection(career_skills))
    missing_skills = list(career_skills.difference(user_skills))

    # Score breakdown
    score_data = score_career(user_input, career)

    # Generate skill gap learning plan
    skill_gap_plan = generate_skill_gap_plan(
        user_input["skills"],
        career
    )

    # Generate roadmap
    roadmap = generate_roadmap(skill_gap_plan)

    return {
        "career": career["name"],
        "match_score": score_data["total_score"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_breakdown": score_data,
        "learning_plan": skill_gap_plan,
        "career_roadmap": roadmap,
        "risk_level": career["risk_level"],
        "market_demand": career["market_demand"],
        "average_salary_lpa": career.get("average_salary_lpa", "Not Available")
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


def generate_skill_gap_plan(user_skills: List[str], career: Dict) -> List[Dict]:
    """
    Generates a structured learning plan for missing skills
    """

    user_skills_set = set(skill.lower() for skill in user_skills)
    required_skills_set = set(skill.lower() for skill in career["required_skills"])

    missing_skills = required_skills_set.difference(user_skills_set)

    learning_plan = []

    for skill in missing_skills:

        # Get learning resource if available
        learning_focus = career.get("learning_paths", {}).get(
            skill,
            "Structured learning required"
        )

        # Estimate difficulty (basic heuristic)
        if skill in ["communication", "general knowledge"]:
            difficulty = "Low"
            estimated_time = "1-2 Months"
        elif skill in ["python", "statistics", "analysis"]:
            difficulty = "Medium"
            estimated_time = "2-3 Months"
        else:
            difficulty = "High"
            estimated_time = "3-4 Months"

        learning_plan.append({
            "skill_to_learn": skill,
            "recommended_focus": learning_focus,
            "difficulty_level": difficulty,
            "estimated_timeline": estimated_time
        })

    # Optional: sort by difficulty priority (High first)
    difficulty_order = {"High": 1, "Medium": 2, "Low": 3}
    learning_plan.sort(key=lambda x: difficulty_order[x["difficulty_level"]])

    return learning_plan


def generate_roadmap(skill_gap_plan: List[Dict]) -> Dict:
    roadmap = {
        "Phase 1 (Month 1-2)": [],
        "Phase 2 (Month 3-5)": [],
        "Phase 3 (Month 6-9)": [],
        "Phase 4 (Month 10-12)": [
            "Build portfolio projects",
            "Apply for internships / real-world opportunities",
            "Optimize resume & LinkedIn"
        ]
    }

    if not skill_gap_plan:
        roadmap["Phase 1 (Month 1-2)"].append("Strengthen core fundamentals")
        roadmap["Phase 2 (Month 3-5)"].append("Build intermediate projects")
        roadmap["Phase 3 (Month 6-9)"].append("Develop specialization & advanced projects")
        return roadmap

    for skill_item in skill_gap_plan:
        skill = skill_item["skill_to_learn"]

        # Phase 1 – Learn Fundamentals
        roadmap["Phase 1 (Month 1-2)"].append(
            f"Learn fundamentals of {skill}"
        )

        # Phase 2 – Apply Practically
        roadmap["Phase 2 (Month 3-5)"].append(
            f"Build practical projects using {skill}"
        )

        # Phase 3 – Mastery & Specialization
        roadmap["Phase 3 (Month 6-9)"].append(
            f"Advanced specialization & optimization in {skill}"
        )

    return roadmap
# recommendation_engine.py

from typing import List, Dict
from app.services.career_database import CAREER_DATABASE


# ----------------------------
# Utility Functions
# ----------------------------

def calculate_skill_match(user_skills: List[str], career_skills: List[str]) -> float:
    matches = set(user_skills).intersection(set(career_skills))
    return len(matches) / len(career_skills)


def calculate_interest_match(user_interests: List[str], career_interests: List[str]) -> float:
    matches = set(user_interests).intersection(set(career_interests))
    return len(matches) / len(career_interests)


# ----------------------------
# Scoring Logic
# ----------------------------

def score_career(user_input: Dict, career: Dict) -> Dict:

    breakdown = {}

    # Skill Score (35%)
    skill_score_raw = calculate_skill_match(
        user_input["skills"],
        career["required_skills"]
    )
    skill_score = skill_score_raw * 35
    breakdown["skill_score"] = round(skill_score, 2)

    # Interest Score (20%)
    interest_score_raw = calculate_interest_match(
        user_input["interests"],
        career["related_interests"]
    )
    interest_score = interest_score_raw * 20
    breakdown["interest_score"] = round(interest_score, 2)

    # Growth / Stability (25%)
    if user_input["career_mode"] == "growth":
        pref_score = career["growth_score"] * 2.5
        breakdown["mode_type"] = "growth"
    else:
        pref_score = career["stability_score"] * 2.5
        breakdown["mode_type"] = "stability"

    breakdown["growth_or_stability_score"] = round(pref_score, 2)

    # Market Demand (20%)
    market_score = career["market_demand"] * 2
    breakdown["market_score"] = round(market_score, 2)

    # Risk Alignment
    user_risk = user_input["risk_preference"]

    if user_risk == "low":
        risk_alignment = 10 - abs(career["risk_level"] - 2)
    elif user_risk == "medium":
        risk_alignment = 10 - abs(career["risk_level"] - 5)
    else:
        risk_alignment = 10 - abs(career["risk_level"] - 8)

    breakdown["risk_alignment_score"] = round(risk_alignment, 2)

    # Total Score
    total_score = (
        skill_score +
        interest_score +
        pref_score +
        market_score +
        risk_alignment
    )

    breakdown["total_score"] = round(total_score, 2)

    return breakdown


# ----------------------------
# AI Explanation Logic
# ----------------------------

def generate_ai_explanation(user_input: Dict, career: Dict) -> str:

    explanation = (
        f"Based on your interests in {', '.join(user_input['interests'])} "
        f"and your current skills in {', '.join(user_input['skills'])}, "
        f"the role of {career['name']} aligns well with your selected "
        f"'{user_input['career_mode']}' mode preference.\n\n"
        f"This career offers {career['future_scope']} "
        f"It follows a work style focused on {career['work_style']}, "
        f"and current industry trends indicate: {career['industry_trend']}."
    )

    return explanation


def generate_career_advantages(career: Dict) -> List[str]:

    advantages = [
        f"High market demand score of {career['market_demand']}/10",
        f"Strong salary potential of ₹{career['average_salary_lpa']} LPA",
        f"Growth score rated {career['growth_score']}/10",
        f"Industry category: {career['category']}"
    ]

    return advantages


# ----------------------------
# Main Career Analysis
# ----------------------------

def analyze_career(user_input: Dict, career: Dict) -> Dict:

    user_skills = set(user_input["skills"])
    career_skills = set(career["required_skills"])

    matched_skills = list(user_skills.intersection(career_skills))
    missing_skills = list(career_skills.difference(user_skills))

    score_data = score_career(user_input, career)

    skill_gap_plan = generate_skill_gap_plan(
        user_input["skills"],
        career
    )

    roadmap = generate_roadmap(skill_gap_plan)

    ai_explanation = generate_ai_explanation(user_input, career)
    advantages = generate_career_advantages(career)

    return {
        "career": career["name"],
        "match_score": score_data["total_score"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_breakdown": score_data,
        "learning_plan": skill_gap_plan,
        "career_roadmap": roadmap,
        "risk_level": career["risk_level"],
        "market_demand": career["market_demand"],
        "average_salary_lpa": career.get("average_salary_lpa", "Not Available"),
        "ai_explanation": ai_explanation,
        "career_advantages": advantages
    }


# ----------------------------
# Recommendation Engine
# ----------------------------

def recommend_careers(user_input: Dict) -> Dict:

    analyzed_results = []

    for career in CAREER_DATABASE:
        analysis = analyze_career(user_input, career)
        analyzed_results.append(analysis)

    analyzed_results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "primary_recommendation": analyzed_results[0],
        "backup_recommendation": analyzed_results[1]
    }


# ----------------------------
# Skill Gap Plan
# ----------------------------

def generate_skill_gap_plan(user_skills: List[str], career: Dict) -> List[Dict]:

    user_skills_set = set(skill.lower() for skill in user_skills)
    required_skills_set = set(skill.lower() for skill in career["required_skills"])

    missing_skills = required_skills_set.difference(user_skills_set)

    learning_plan = []

    for skill in missing_skills:

        learning_focus = career.get("learning_paths", {}).get(
            skill,
            "Structured learning required"
        )

        if skill in ["communication", "general knowledge"]:
            difficulty = "Low"
            estimated_time = "1-2 Months"
        elif skill in ["python", "statistics", "analysis"]:
            difficulty = "Medium"
            estimated_time = "2-3 Months"
        else:
            difficulty = "High"
            estimated_time = "3-4 Months"

        learning_plan.append({
            "skill_to_learn": skill,
            "recommended_focus": learning_focus,
            "difficulty_level": difficulty,
            "estimated_timeline": estimated_time
        })

    difficulty_order = {"High": 1, "Medium": 2, "Low": 3}
    learning_plan.sort(key=lambda x: difficulty_order[x["difficulty_level"]])

    return learning_plan


# ----------------------------
# Roadmap Generator
# ----------------------------

def generate_roadmap(skill_gap_plan: List[Dict]) -> Dict:

    roadmap = {
        "Phase 1 (Month 1-2)": [],
        "Phase 2 (Month 3-5)": [],
        "Phase 3 (Month 6-9)": [],
        "Phase 4 (Month 10-12)": [
            "Build portfolio projects",
            "Apply for internships / real-world opportunities",
            "Optimize resume & LinkedIn"
        ]
    }

    if not skill_gap_plan:
        roadmap["Phase 1 (Month 1-2)"].append("Strengthen core fundamentals")
        roadmap["Phase 2 (Month 3-5)"].append("Build intermediate projects")
        roadmap["Phase 3 (Month 6-9)"].append("Develop specialization & advanced projects")
        return roadmap

    for skill_item in skill_gap_plan:
        skill = skill_item["skill_to_learn"]

        roadmap["Phase 1 (Month 1-2)"].append(
            f"Learn fundamentals of {skill}"
        )

        roadmap["Phase 2 (Month 3-5)"].append(
            f"Build practical projects using {skill}"
        )

        roadmap["Phase 3 (Month 6-9)"].append(
            f"Advanced specialization & optimization in {skill}"
        )

    return roadmap
