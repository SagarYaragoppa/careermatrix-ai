import re
import spacy


nlp = spacy.load("en_core_web_sm")


SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "go", "rust", "php", "ruby", "swift", "kotlin", "r", "matlab",

    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "computer vision", "data science", "data analysis",
    "feature engineering", "model training", "model evaluation",

    "tensorflow", "pytorch", "keras", "scikit-learn",
    "xgboost", "lightgbm", "opencv", "nltk", "spacy",
    "hugging face", "transformers",

    "numpy", "pandas", "matplotlib", "seaborn",
    "plotly", "power bi", "tableau", "excel",

    "sql", "mysql", "postgresql", "sqlite",
    "mongodb", "redis", "oracle", "firebase",

    "html", "css", "react", "angular", "vue",
    "node.js", "express.js", "django", "flask", "fastapi",
    "rest api", "graphql",

    "git", "github", "gitlab", "docker", "kubernetes",
    "aws", "azure", "google cloud", "ci/cd",
    "linux", "bash", "powershell",

    "data structures", "algorithms", "object oriented programming",
    "operating systems", "computer networks",
    "database management systems", "software engineering",
    "system design"
]


SECTION_HEADERS = [
    "education", "academic background", "academics", "qualifications",
    "experience", "work experience", "professional experience",
    "employment", "internship", "internships",
    "skills", "technical skills", "skill set",
    "projects", "project experience",
    "certifications", "achievements",
    "research", "publications",
    "summary", "profile", "objective",
    "interests", "hobbies"
]

EDUCATION_HEADERS = [
    "education", "academic background", "academics", "qualifications","EDUCATION"
]

EXPERIENCE_HEADERS = [
    "experience", "work experience", "professional experience",
    "employment", "internship", "internships"
]

def normalize_line(line: str) -> str:
    return re.sub(r'[^a-z ]', '', line.lower()).strip()


def extract_name(text: str):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_email(text: str):
    match = re.search(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        text
    )
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(
        r'(\+?\d{1,3}[\s-]?)?\d{10}',
        text
    )
    return match.group(0) if match else None



def extract_skills(text: str):
    text = text.lower()
    found = set()

    for skill in SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)

    return list(found)



def extract_section(text: str, target_headers: list):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    content = []
    capture = False

    for line in lines:
        normalized = re.sub(r'[^a-z ]', '', line.lower()).strip()

        
        if not capture and any(h in normalized for h in target_headers):
            capture = True
            continue

        
        if capture and any(
            h in normalized
            for h in SECTION_HEADERS
            if h not in target_headers
        ):
            break

        if capture:
            content.append(line)

    return content



def extract_education(text: str):
    text = text.lower()

    pattern = re.compile(
        r'education(.*?)(skills|projects|experience|certification|objective|$)',
        re.DOTALL
    )

    match = pattern.search(text)
    if not match:
        return []

    edu_block = match.group(1)

    # Clean and split
    lines = [line.strip() for line in edu_block.split("\n") if line.strip()]
    return lines


def extract_experience(text: str):
    text = text.lower()

    pattern = re.compile(
        r'(experience|work experience|internship)(.*?)(education|skills|projects|certification|objective|$)',
        re.DOTALL
    )

    match = pattern.search(text)
    if not match:
        return []

    exp_block = match.group(2)

    lines = [line.strip() for line in exp_block.split("\n") if line.strip()]
    return lines





def parse_resume(text: str) -> dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
