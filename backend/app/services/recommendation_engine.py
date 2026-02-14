# recommendation_engine.py

from typing import List, Dict
from app.services.career_database import CAREER_DATABASE


# ----------------------------
# Sample Career Dataset
# ----------------------------

# career_database.py

CAREER_DATABASE = [

    {
        "name": "Machine Learning Engineer",
        "required_skills": ["python", "math", "machine learning"],
        "related_interests": ["ai", "technology", "research"],
        "growth_score": 9,
        "stability_score": 7,
        "market_demand": 9,
        "risk_level": 6,
        "average_salary_lpa": 15,
        "learning_paths": {
            "python": "Advanced Python + DSA practice",
            "math": "Linear Algebra, Probability & Statistics",
            "machine learning": "Supervised/Unsupervised ML + real-world projects"
        }
    },

    {
        "name": "Data Scientist",
        "required_skills": ["python", "statistics", "machine learning"],
        "related_interests": ["data", "ai", "analysis"],
        "growth_score": 9,
        "stability_score": 8,
        "market_demand": 8,
        "risk_level": 5,
        "average_salary_lpa": 18,
        "learning_paths": {
            "python": "Data libraries (Pandas, NumPy)",
            "statistics": "Hypothesis testing & distributions",
            "machine learning": "Model building + deployment"
        }
    },

    {
        "name": "Software Developer",
        "required_skills": ["programming", "problem solving", "data structures"],
        "related_interests": ["technology", "building products"],
        "growth_score": 8,
        "stability_score": 8,
        "market_demand": 9,
        "risk_level": 4,
        "average_salary_lpa": 12,
        "learning_paths": {
            "programming": "Master one core language",
            "problem solving": "LeetCode + Competitive Programming",
            "data structures": "DSA fundamentals"
        }
    },

    {
        "name": "Cybersecurity Analyst",
        "required_skills": ["networking", "security fundamentals", "linux"],
        "related_interests": ["security", "technology", "investigation"],
        "growth_score": 8,
        "stability_score": 9,
        "market_demand": 8,
        "risk_level": 4,
        "average_salary_lpa": 10,
        "learning_paths": {
            "networking": "TCP/IP, OSI Model",
            "security fundamentals": "Ethical hacking basics",
            "linux": "Linux administration & commands"
        }
    },

    {
        "name": "Investment Banker",
        "required_skills": ["finance", "analysis", "communication"],
        "related_interests": ["finance", "markets", "business"],
        "growth_score": 9,
        "stability_score": 6,
        "market_demand": 7,
        "risk_level": 8,
        "average_salary_lpa": 20,
        "learning_paths": {
            "finance": "Corporate finance fundamentals",
            "analysis": "Financial modeling",
            "communication": "Presentation & negotiation skills"
        }
    },

    {
        "name": "Product Manager",
        "required_skills": ["communication", "strategy", "market analysis"],
        "related_interests": ["business", "technology", "leadership"],
        "growth_score": 8,
        "stability_score": 7,
        "market_demand": 8,
        "risk_level": 6,
        "average_salary_lpa": 22,
        "learning_paths": {
            "communication": "Stakeholder management",
            "strategy": "Product lifecycle management",
            "market analysis": "Customer research & data interpretation"
        }
    },

    {
        "name": "Government Officer",
        "required_skills": ["general knowledge", "administration"],
        "related_interests": ["public service", "governance"],
        "growth_score": 6,
        "stability_score": 10,
        "market_demand": 6,
        "risk_level": 2,
        "average_salary_lpa": 8,
        "learning_paths": {
            "general knowledge": "Current affairs + polity",
            "administration": "Public policy & governance basics"
        }
    },

    {
        "name": "Digital Marketing Specialist",
        "required_skills": ["communication", "seo", "analytics"],
        "related_interests": ["business", "branding", "creativity"],
        "growth_score": 8,
        "stability_score": 7,
        "market_demand": 8,
        "risk_level": 5,
        "average_salary_lpa": 9,
        "learning_paths": {
            "seo": "Search engine optimization fundamentals",
            "analytics": "Google Analytics + performance tracking",
            "communication": "Copywriting & branding"
        }
    }
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
    """
    Generates a structured 6–12 month roadmap
    based on missing skill priority
    """

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

    # If no missing skills → advanced growth roadmap
    if not skill_gap_plan:
        roadmap["Phase 1 (Month 1-2)"].append(
            "Start building advanced real-world projects"
        )
        roadmap["Phase 2 (Month 3-5)"].append(
            "Contribute to open-source or freelance work"
        )
        return roadmap

    # Assign skills to phases
    for i, skill_item in enumerate(skill_gap_plan):

        skill_name = skill_item["skill_to_learn"]

        if i < 2:
            roadmap["Phase 1 (Month 1-2)"].append(
                f"Master {skill_name}"
            )

        elif i < 4:
            roadmap["Phase 2 (Month 3-5)"].append(
                f"Advance proficiency in {skill_name}"
            )

        else:
            roadmap["Phase 3 (Month 6-9)"].append(
                f"Deep specialization in {skill_name}"
            )

    return roadmap


