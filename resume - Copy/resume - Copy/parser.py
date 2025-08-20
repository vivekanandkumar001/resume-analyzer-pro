# === parser.py — Improved Resume Parser ===
import re
import pdfplumber
import docx

def extract_text(file):
    """Extract raw text from pdf, docx, or txt"""
    name = file.name.lower()
    if name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    elif name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")

    return ""


def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r"(\\+\\d{1,3}[- ]?)?\\d{10}", text)
    return match.group(0) if match else None


def extract_name(text):
    # Heuristic: assume name is the first line with 2+ words, all letters
    for line in text.splitlines():
        if line.strip() and len(line.split()) <= 4 and line[0].isupper():
            return line.strip()
    return None


def extract_skills(text):
    skill_keywords = [
        "python", "java", "c++", "sql", "tensorflow", "keras", "pytorch",
        "excel", "hadoop", "spark", "nlp", "machine learning", "deep learning",
        "html", "css", "javascript", "react", "angular", "node", "git", "docker", "aws"
    ]
    skills_found = []
    for skill in skill_keywords:
        if re.search(rf"\\b{skill}\\b", text, re.IGNORECASE):
            skills_found.append(skill.capitalize())
    return list(set(skills_found))


def extract_education(text):
    edu_keywords = ["b.tech", "m.tech", "bachelor", "master", "phd",
                    "degree", "university", "college", "school", "diploma"]
    education = []
    for line in text.splitlines():
        if any(word in line.lower() for word in edu_keywords):
            education.append(line.strip())
    return education


def extract_experience(text):
    exp_keywords = ["intern", "engineer", "developer", "manager", "analyst",
                    "consultant", "research", "project", "experience", "work"]
    experience = []
    for line in text.splitlines():
        if any(word in line.lower() for word in exp_keywords):
            experience.append(line.strip())
    return experience


def parse_resume(file):
    """Main function: parse resume into structured fields"""
    text = extract_text(file)
    if not text:
        return {}

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "summary": text[:500],  # crude: first 500 chars as summary
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "extras": []
    }
