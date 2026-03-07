# CareerMatrix AI 🚀 – Intelligent Career Recommendation & Resume Intelligence Platform

CareerMatrix AI is an AI-powered platform designed to assist students and professionals in making better career decisions. The system combines **career recommendation algorithms**, **resume parsing**, **skill analysis**, and **job matching techniques** to provide actionable insights about career paths and resume quality.

The project demonstrates practical applications of **Artificial Intelligence, Natural Language Processing (NLP), and Data Processing** to solve real-world problems in career planning and recruitment.

---

# Table of Contents

* Project Overview
* Key Features
* System Architecture
* Modules Explained
* Career Recommendation Engine
* Resume Intelligence System
* Resume Parsing Engine
* Resume Scoring System
* Candidate Summary Generator
* Job Description Matching
* Technology Stack
* Project Structure
* Installation Guide
* Usage Guide
* Future Improvements
* Author

---

# Project Overview

Choosing the right career path can be difficult due to lack of proper guidance and understanding of skill requirements. Similarly, recruiters often spend significant time analyzing resumes to determine candidate suitability.

CareerMatrix AI addresses both problems by providing:

1. **AI-based career recommendations**
2. **Automated resume analysis**
3. **Skill extraction and evaluation**
4. **Resume scoring**
5. **Job-skill matching analysis**
6. **Candidate summaries for quick evaluation**

The system uses **machine learning concepts, NLP-based information extraction, and rule-based scoring algorithms** to generate insights from user inputs and resumes.

---

# Key Features

### Career Recommendation System

* Suggests suitable career paths based on:

  * Interests
  * Skills
  * Work style
  * Risk appetite
  * Learning preferences
* Provides **primary career recommendation** and **backup career option**.

### Resume Intelligence System

* Upload resume (PDF)
* Extract structured information
* Evaluate resume quality
* Provide skill insights

### Resume Parsing

Automatically extracts:

* Name
* Email
* Phone number
* Skills
* Education
* Experience
* Projects

### Resume Scoring

Evaluates resume strength based on:

* Skills
* Projects
* Experience
* Education

Final score is calculated out of **100 points**.

### Candidate Summary Generator

Automatically generates a short summary describing the candidate profile.

Example:

> Ajay Pandey has strong skills in Python and Machine Learning. The candidate has completed 1 project and has internship experience. Academic background information was detected.

### Job Description Matching

Users can enter job-related skills.

The system compares:

* Resume skills
* Job skills

And generates:

* Match Score
* Matched Skills
* Missing Skills

### Career Alignment Indicator

Shows how well the candidate fits certain roles like:

* AI/ML Engineer
* Data Analyst
* Backend Developer

---

# System Architecture

The project follows a **full-stack architecture**.

```
React Frontend
      |
      | HTTP API
      |
FastAPI Backend
      |
Resume Processing Pipeline
      |
NLP Extraction + Scoring Engine
```

---

# Modules Explained

The system is divided into two main modules:

## 1. CareerMatrix (Career Recommendation)

Provides career suggestions based on user input.

### Inputs

* Interests
* Skills
* Work style
* Learning preference
* Risk tolerance

### Output

* Primary career recommendation
* Backup career option
* Match score
* Salary estimate

---

## 2. Resume Intelligence System

This module analyzes resumes using NLP and rule-based algorithms.

It includes several submodules.

---

# Resume Parsing Engine

The parser extracts structured information from resumes.

### Technologies used

* Regular Expressions
* NLP using **spaCy**
* Text pattern matching

### Extraction methods

| Data Type  | Method                           |
| ---------- | -------------------------------- |
| Name       | Named Entity Recognition (spaCy) |
| Email      | Regex pattern                    |
| Phone      | Regex pattern                    |
| Skills     | Keyword dictionary matching      |
| Education  | Section detection                |
| Experience | Section detection                |
| Projects   | Section detection                |

---

# Resume Scoring System

The scoring system evaluates resume quality using a point-based system.

### Scoring Criteria

| Category   | Maximum Score |
| ---------- | ------------- |
| Skills     | 40            |
| Projects   | 15            |
| Experience | 25            |
| Education  | 20            |

### Score Calculation

```
Resume Score =
Skills Score +
Projects Score +
Experience Score +
Education Score
```

Final score is normalized to **100 points**.

---

# Candidate Summary Generator

This module generates a short natural-language description of the candidate profile.

It analyzes:

* Skills detected
* Number of projects
* Work experience
* Education

The output provides a quick overview for recruiters.

---

# Job Description Matching

This module compares resume skills with job requirements.

### Input

Job-related skills entered by the user.

Example:

```
python, machine learning, tensorflow
```

### Process

1. Extract resume skills
2. Convert job skills into list
3. Compare overlap

### Output

* Match Score
* Matched Skills
* Missing Skills

Example:

```
Match Score: 66%

Matched Skills:
python, machine learning

Missing Skills:
tensorflow
```

---

# Technology Stack

## Frontend

* React.js
* Tailwind CSS
* JavaScript
* Fetch API

## Backend

* FastAPI
* Python

## AI / NLP

* spaCy
* Regex
* Text processing

## Resume Processing

* PDF text extraction
* Text cleaning
* Pattern-based information extraction

---

# Project Structure

```
careermatrix-ai
│
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── resume_parser
│   │   │   ├── extractor.py
│   │   │   ├── pdf_reader.py
│   │   │   ├── text_cleaner.py
│   │   │   ├── resume_scoring.py
│   │   │   └── pipeline.py
│   │
│   ├── uploads
│   └── venv
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   │   ├── Dashboard.js
│   │   │   └── ResumeParser.js
│   │   ├── App.js
│   │   └── index.js
│
└── README.md
```

---

# Installation Guide

## Clone Repository

```
git clone https://github.com/yourusername/careermatrix-ai.git
```

---

## Backend Setup

Navigate to backend folder

```
cd backend
```

Create virtual environment

```
python -m venv venv
```

Activate environment

```
venv\Scripts\activate
```

Install dependencies

```
pip install fastapi uvicorn spacy python-multipart
```

Download spaCy model

```
python -m spacy download en_core_web_sm
```

Run backend server

```
python -m uvicorn app.main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Navigate to frontend folder

```
cd frontend
```

Install dependencies

```
npm install
```

Run frontend

```
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

# Usage Guide

### Career Recommendation

1. Open dashboard
2. Enter:

   * interests
   * skills
   * work style
   * risk tolerance
3. Click **Get Recommendation**

The system returns:

* Primary career
* Backup career
* Match score

---

### Resume Analysis

1. Open Resume Intelligence page
2. Upload resume
3. Enter job skills (optional)
4. Click **Upload Resume**

System returns:

* Resume score
* Skills
* Education
* Experience
* Projects
* Candidate summary
* Job match analysis

---

# Future Improvements

Possible improvements include:

* Machine learning based career prediction
* Deep learning resume understanding
* Resume skill gap suggestions
* Job recommendation system
* Resume improvement suggestions
* Resume ranking for recruiters
* Integration with LinkedIn or job portals
* Resume ATS compatibility checker

---

# Author

Sagar Ramesh Yaragoppa
Sahil Kadaskar
Rugved Narendra Bhandarkar
Kavya Patel
Sneha Satarke
Shreya Diliprao Thakare
Lathisha Padayachi
Yash Sudam Ukirde
Kshitij Shrikhande
Khushal Moundekar

This project was developed as part of an academic and practical exploration of AI applications in career guidance and recruitment systems.


