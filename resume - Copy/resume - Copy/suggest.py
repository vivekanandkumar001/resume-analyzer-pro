
import csv
import os
import json
from datetime import datetime
from categories import CATEGORY_SKILLS

ALL_ROLES = list(CATEGORY_SKILLS.keys())
ROLE_SKILLS = CATEGORY_SKILLS

FEEDBACK_LOG = "feedback_log.csv"
POS_FILE = "feedback_positive.csv"
NEG_FILE = "feedback_negative.csv"
RL_WEIGHTS_FILE = "rl_weights.json"  # optional biasing
def _load_rl_weights():
    if os.path.exists(RL_WEIGHTS_FILE):
        try:
            return json.load(open(RL_WEIGHTS_FILE, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _rank_with_weights(items):
    """Optionally re-rank items by lightweight RL weights (descending)."""
    w = _load_rl_weights()
    def score(x):
        key = (x or "").lower()
        return float(w.get(key, 0.0))
    return sorted(items, key=score, reverse=True)


def analyze_for_role(resume_text: str, role: str):
    """Return structured suggestions for a given role."""
    role_skills = ROLE_SKILLS.get(role, [])
    text_lower = (resume_text or "").lower()

    missing = [s for s in role_skills if s.lower() not in text_lower]
    missing = _rank_with_weights(missing)

    projects = [f"Build a mini project using {s}" for s in missing]
    courses = [f"Take an online course in {s}" for s in missing]
    certs = [f"Certification in {s}" for s in missing]

    return {
        "missing_skills": missing,
        "projects": projects,
        "courses": courses,
        "certificates": certs,
        "improvements": [
            "Make skills section more detailed (bullet points).",
            "Add measurable achievements (numbers, %, time).",
            "Place most relevant projects at the top for the target role."
        ],
    }


def suggest_from_resume(resume_text: str, role: str):
    result = analyze_for_role(resume_text, role)
    return {
        "missing_skills": result["missing_skills"],
        "suggestions": [
            {"project_title": f"Practice project: {s}"} for s in result["missing_skills"]
        ],
    }


def log_feedback_rows(resume_id: str, target_role: str, rows, reward: int, comments: str = ""):
    """Log feedback into feedback_log.csv and split into positive/negative CSVs."""
    log_exists = os.path.exists(FEEDBACK_LOG)
    pos_exists = os.path.exists(POS_FILE)
    neg_exists = os.path.exists(NEG_FILE)

    # open master + split file
    with open(FEEDBACK_LOG, "a", newline="", encoding="utf-8") as log_f,          open(POS_FILE if reward > 0 else NEG_FILE, "a", newline="", encoding="utf-8") as fb_f:

        fieldnames = ["timestamp", "resume_id", "role", "kind", "text", "reward", "comments"]
        log_writer = csv.DictWriter(log_f, fieldnames=fieldnames)
        fb_writer = csv.DictWriter(fb_f, fieldnames=fieldnames)

        if not log_exists:
            log_writer.writeheader()
        if reward > 0 and not pos_exists:
            fb_writer.writeheader()
        if reward < 0 and not neg_exists:
            fb_writer.writeheader()

        ts = datetime.utcnow().isoformat()

        for kind, text in rows:
            row = {
                "timestamp": ts,
                "resume_id": resume_id,
                "role": target_role,
                "kind": kind,
                "text": text,
                "reward": reward,
                "comments": comments or ""
            }
            log_writer.writerow(row)
            fb_writer.writerow(row)

    return True
# ==============================
# suggest.py
# ==============================
import os
import re
import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

# ==============================
# Role → Required Skills mapping
# ==============================
ROLE_SKILLS: Dict[str, List[str]] = {
    "data scientist": ["python","sql","statistics","machine learning","deep learning","pandas","numpy","nlp"],
    "software engineer": ["python","java","c++","git","system design","databases","algorithms","data structures"],
    "web developer": ["html","css","javascript","react","node.js","mongodb","api","git"],
    "ml engineer": ["python","tensorflow","pytorch","scikit-learn","mlops","docker","aws","azure","kubernetes"],

    # --- AI Categories (general + specialized) ---
    "ai": ["python","pytorch","tensorflow","transformers","huggingface","mlflow","docker","fastapi","aws","azure"],
    "ai engineer": ["python","pytorch","tensorflow","transformers","huggingface","mlflow","docker","fastapi","prompt engineering","aws","gcp","azure"],
    "ai researcher": ["python","pytorch","tensorflow","deep learning","transformers","statistics","experimentation","numpy","scipy"],

    # --- LLM & NLP ---
    "llm engineer": ["python","transformers","huggingface","prompt engineering","rag","vector dbs","langchain","pytorch","mlflow","docker","aws"],
    "nlp engineer": ["python","nlp","transformers","huggingface","spacy","nltk","text classification","bert","gpt"],

    # --- CV ---
    "computer vision engineer": ["python","opencv","cnn","pytorch","tensorflow","image processing","object detection","segmentation"],

    # --- Generative AI ---
    "generative ai": ["python","pytorch","tensorflow","transformers","diffusion models","huggingface","mlflow","docker","stable diffusion","dalle","midjourney"],
    "generative ai engineer": ["python","pytorch","tensorflow","transformers","diffusion models","huggingface","mlflow","docker","prompt engineering","gan","vae","stable diffusion","text-to-image","text-to-video"],
}

# ==============================
# Suggestions Data Structures
# ==============================
@dataclass
class Suggestion:
    skill: str
    project_title: str
    course: str
    certificate: str

@dataclass
class SuggestionResult:
    missing_skills: List[str]
    suggestions: List[Suggestion]

# ==============================
# Helpers
# ==============================
def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).strip()

def _extract_resume_skills(resume_text: str) -> List[str]:
    resume_text = _normalize(resume_text or "")
    found: List[str] = []
    for skills in ROLE_SKILLS.values():
        for s in skills:
            if s in resume_text and s not in found:
                found.append(s)
    return found

def _canonical_role(target_role: str) -> str:
    t = _normalize(target_role or "")
    if not t:
        return "software engineer"

    # direct shortcuts
    if t == "ai":
        return "ai"
    if "llm" in t:
        return "llm engineer"
    if "generative ai" in t and "engineer" not in t:
        return "generative ai"
    if "generative" in t and "ai" in t:
        return "generative ai engineer"

    candidates = list(ROLE_SKILLS.keys())
    scores: List[Tuple[int, str]] = []
    for r in candidates:
        score = 0
        for token in r.split():
            if token in t:
                score += 2
        if "ai" in t and r in {"ai","ai engineer","ai researcher","ml engineer"}:
            score += 3
        if "nlp" in t and r == "nlp engineer":
            score += 3
        if "vision" in t and r == "computer vision engineer":
            score += 3
        scores.append((score, r))
    scores.sort(reverse=True)
    return scores[0][1] if scores and scores[0][0] > 0 else "software engineer"

# ==============================
# Dynamic Courses & Certificates
# ==============================
COURSES = {
    "python": "Complete Python Bootcamp (Udemy)",
    "tensorflow": "DeepLearning.AI TensorFlow Developer (Coursera)",
    "pytorch": "DeepLearning.AI PyTorch for Deep Learning (Coursera)",
    "transformers": "Hugging Face Transformers Course",
    "mlops": "MLOps Specialization (Coursera)",
    "docker": "Docker Essentials (IBM Skills)",
    "aws": "AWS Machine Learning Specialty",
    "azure": "Azure AI Engineer Associate Path",
    "generative ai": "Generative AI with Diffusion Models (Coursera)",
    "nlp": "Natural Language Processing Specialization (Coursera)",
}

CERTIFICATES = {
    "python": "PCAP – Certified Associate in Python Programming",
    "tensorflow": "TensorFlow Developer Certificate",
    "pytorch": "Meta AI PyTorch Certification",
    "mlops": "Certified MLOps Professional",
    "aws": "AWS Certified AI Practitioner",
    "azure": "Microsoft Certified: Azure AI Engineer Associate",
    "generative ai": "Generative AI by DeepLearning.AI",
    "nlp": "Specialization in NLP by Stanford",
}

# ==============================
# Core Suggestion Logic
# ==============================
def suggest_from_resume(resume_text: str, target_role: str) -> SuggestionResult:
    resume_skills = _extract_resume_skills(resume_text)
    role = _canonical_role(target_role)
    required = ROLE_SKILLS.get(role, [])
    missing = [s for s in required if s not in resume_skills]

    suggestions: List[Suggestion] = []
    for s in missing:
        project_title = f"Build a project demonstrating {s.title()} for a {role.title()} role"
        course = COURSES.get(s, f"Take an advanced course in {s.title()}")
        certificate = CERTIFICATES.get(s, f"Earn a certificate in {s.title()}")
        suggestions.append(Suggestion(s, project_title, course, certificate))

    return SuggestionResult(missing, suggestions)

# ==============================
# Feedback Logging
# ==============================
def _ensure_file(path: str, header: List[str]):
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)

def log_feedback(resume_id: str, target_role: str, suggestion: Suggestion, reward: int, comments: str = ""):
    row = [resume_id, target_role, suggestion.skill, suggestion.project_title, suggestion.course, suggestion.certificate, reward, comments]
    header = ["resume_id", "target_role", "skill", "project_title", "course", "certificate", "reward", "comments"]

    # general log
    _ensure_file("feedback_log.csv", header)
    with open("feedback_log.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

    # pos/neg split logs
    if reward > 0:
        path = "positive_feedback.csv"
    else:
        path = "negative_feedback.csv"
    _ensure_file(path, header)
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

# ==============================
# Role Analysis Wrapper
# ==============================
def analyze_for_role(resume_text: str, target_role: str) -> dict:
    """
    Analyze resume for a target role and return improvements, missing skills,
    projects, courses, and certificates.
    """
    result = suggest_from_resume(resume_text, target_role)

    improvements = []
    if len(resume_text.split()) < 200:
        improvements.append("Expand your resume with more details on projects, achievements, and skills.")
    if not any(word in resume_text.lower() for word in ["experience", "project", "internship"]):
        improvements.append("Add a section for Experience, Projects, or Internships.")
    if not any(word in resume_text.lower() for word in ["education", "bachelor", "master", "degree"]):
        improvements.append("Include your Education details.")

    return {
        "improvements": improvements,
        "missing_skills": result.missing_skills,
        "projects": [s.project_title for s in result.suggestions],
        "courses": [s.course for s in result.suggestions],
        "certificates": [s.certificate for s in result.suggestions],
    }

# ==============================
# Export roles list
# ==============================
ALL_ROLES = list(ROLE_SKILLS.keys())
def get_all_roles() -> List[str]:
    """Return a sorted list of all available roles."""
    return sorted(ALL_ROLES)