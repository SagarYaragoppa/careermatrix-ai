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

PROJECT_HEADERS = [
    "projects",
    "project",
    "academic projects",
    "personal projects",
    "key projects",
    "project experience"
]

EXPERIENCE_HEADERS = [
    "experience", "work experience", "professional experience",
    "employment", "internship", "internships"
]

def normalize_line(line: str) -> str:
    return re.sub(r'[^a-z ]', '', line.lower()).strip()


def extract_name(text: str):

    lines = text.split("\n")

    # Look in first 10 lines (names usually appear at top)
    for line in lines[:10]:

        line = line.strip()

        # Only accept 2 words (first name + last name)
        words = line.split()

        if len(words) == 2 and all(w.istitle() for w in words):
            return f"{words[0]} {words[1]}"

    # fallback to spaCy
    doc = nlp(text[:500])

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.split()
            return " ".join(name[:2])  # only keep first two words

    return None

def extract_email(text: str):

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    matches = re.findall(email_pattern, text)

    return matches[0] if matches else None


def extract_phone(text: str):

    phone_pattern = r'\b\d{10}\b'

    match = re.search(phone_pattern, text)

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

def extract_projects(text: str):

    lines = text.split("\n")

    projects = []
    capture = False

    for line in lines:

        normalized = line.lower().strip()

        # detect project section
        if "project" in normalized:
            capture = True
            continue

        if capture:

            # stop when next section appears
            if any(
                header in normalized
                for header in SECTION_HEADERS
                if "project" not in header
            ):
                break

            if line.strip():
                projects.append(line.strip())

    return projects

def extract_projects(text: str):

    projects = []

    # find PROJECT / PROJECTS section
    pattern = re.compile(
        r'(project|projects)(.*?)(education|experience|skills|certification|objective|$)',
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(text)

    if not match:
        return []

    project_block = match.group(2)

    lines = project_block.split("\n")

    for line in lines:

        line = line.strip()

        # ignore empty lines
        if not line:
            continue

        # ignore long description lines
        if len(line.split()) <= 6:
            projects.append(line)

    return list(set(projects))

def parse_resume(text: str) -> dict:
    text = text.replace("\xa0", " ")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text)   # NEW
    }

def calculate_resume_score(data: dict):

    score = 0
    breakdown = {}

    # Skills Score
    skills = data.get("skills", [])
    skill_score = min(len(skills) * 5, 40)
    breakdown["skills"] = skill_score
    score += skill_score

    # Projects Score
    projects = data.get("projects", [])
    project_score = min(len(projects) * 10, 25)
    breakdown["projects"] = project_score
    score += project_score

    # Experience Score
    experience = data.get("experience", [])
    experience_score = 20 if experience else 0
    breakdown["experience"] = experience_score
    score += experience_score

    # Education Score
    education = data.get("education", [])
    education_score = 15 if education else 0
    breakdown["education"] = education_score
    score += education_score

    return score, breakdown

def generate_candidate_summary(data: dict):

    name = data.get("name", "The candidate")
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    experience = data.get("experience", [])
    education = data.get("education", [])

    summary = []

    # Skills summary
    if skills:
        top_skills = ", ".join(skills[:3])
        summary.append(f"{name} has strong skills in {top_skills}.")
    else:
        summary.append(f"{name}'s technical skills were not clearly detected.")

    # Projects summary
    if projects:
        summary.append(f"The candidate has completed {len(projects)} project(s).")

    # Experience summary
    if experience:
        summary.append("Professional or internship experience was detected.")
    else:
        summary.append("No professional experience was detected, suggesting an early-career profile.")

    # Education summary
    if education:
        summary.append("Academic background information was detected.")

    return " ".join(summary)

def match_job_description(candidate_skills, job_skills):

    candidate_set = set([s.lower() for s in candidate_skills])
    job_set = set([s.lower().strip() for s in job_skills])

    matched = list(candidate_set.intersection(job_set))
    missing = list(job_set - candidate_set)

    if len(job_set) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_set)) * 100)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score
    }