from .pdf_reader import extract_text_from_pdf
from .text_cleaner import clean_text
from .extractor import parse_resume


def process_resume(file_path: str) -> dict:
    """
    Complete resume processing pipeline:
    PDF → Clean → Extract → Return structured data
    """

    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)
    parsed_data = parse_resume(cleaned_text)

    return {
        "skills": parsed_data.get("skills", []),
        "education": parsed_data.get("education", []),
        "experience": parsed_data.get("experience", [])
    }
