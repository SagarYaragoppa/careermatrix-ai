from .pdf_reader import extract_text_from_pdf
from .text_cleaner import clean_text
from .extractor import (
    parse_resume,
    calculate_resume_score,
    generate_candidate_summary,
    match_job_description
)

def process_resume(file_path: str, job_skills: list = None):

    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)

    parsed_data = parse_resume(cleaned_text)

    score, breakdown = calculate_resume_score(parsed_data)

    summary = generate_candidate_summary(parsed_data)

    job_match = None

    if job_skills:
        job_match = match_job_description(parsed_data["skills"], job_skills)

    return {
        "name": parsed_data.get("name"),
        "email": parsed_data.get("email"),
        "phone": parsed_data.get("phone"),
        "skills": parsed_data.get("skills", []),
        "education": parsed_data.get("education", []),
        "experience": parsed_data.get("experience", []),
        "projects": parsed_data.get("projects", []),

        "resume_score": score,
        "score_breakdown": breakdown,
        "candidate_summary": summary,

        "job_match": job_match
    }