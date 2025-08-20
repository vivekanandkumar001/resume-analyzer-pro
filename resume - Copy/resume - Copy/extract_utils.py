# ===========================================
# extract_utils.py - Resume text extractors
# ===========================================
import io
import re
import pdfplumber
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

# -------- DOCX helpers (preserve tables + paragraphs order) --------
def _iter_block_items(doc):
    body = doc.element.body
    for child in body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)

def _docx_bytes_to_text(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    parts = []
    for block in _iter_block_items(doc):
        if isinstance(block, Paragraph):
            txt = (block.text or "").strip()
            parts.append(txt)
        else:  # Table
            for row in block.rows:
                row_text = "\t".join((cell.text or "").strip() for cell in row.cells)
                parts.append(row_text)
    lines = [p for p in parts if p]
    return "\n".join(lines).strip()

# -------- Public API --------
def extract_text_from_file(uploaded_file) -> str:
    """Extract raw text from PDF/DOCX/TXT. Accepts a Streamlit UploadedFile or any file-like with .name + .read()."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()
    if name.endswith(".pdf"):
        text = []
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for p in pdf.pages:
                t = p.extract_text() or ""
                text.append(t)
        return "\n".join(text).strip()
    if name.endswith(".docx"):
        return _docx_bytes_to_text(raw)
    # txt or others
    try:
        return raw.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

# -------- Field Extractors --------
def extract_name_from_text(text: str, filename: str = "") -> str:
    """Heuristic person-name extractor for resume text."""
    if not text:
        return "Candidate"
    text = re.sub(r"[\u00A0\u200B]+", " ", text)  # normalize spaces
    lines = [l.strip() for l in text.splitlines() if l and l.strip()]

    skip_keywords = {
        "resume", "curriculum vitae", "cv",
        "career objective", "objective", "profile",
        "education", "qualification", "qualifications",
        "skills", "experience", "projects",
        "strength", "hobbies", "achievements", "awards",
        "journal", "publication", "declaration", "contact",
        "email", "mobile", "phone", "address", "linkedin", "github"
    }

    def _is_skip(line: str) -> bool:
        low = line.lower().strip().strip(":")
        return any(k in low for k in skip_keywords)

    top_lines = lines[:20]

    # 1) Strong rule: ALL CAPS 2–3 words near top
    for line in top_lines[:5]:
        if line.isupper() and 1 < len(line.split()) <= 3 and not _is_skip(line):
            return line.title()

    # 2) Proper-cased names
    for line in top_lines:
        if _is_skip(line):
            continue
        if re.match(r"^[A-Z][a-z]+(\s[A-Z]\.)?(\s[A-Z][a-z]+){1,2}$", line):
            return line

    # 3) Backup: capitalized words, 2–3 tokens, no digits/emails
    for line in top_lines:
        if _is_skip(line):
            continue
        if not re.search(r"[\d@:/\\]", line):
            words = line.split()
            if 1 < len(words) <= 3 and sum(1 for w in words if w[0].isupper()) >= 2:
                return line

    # 4) Fallback: filename
    if filename:
        base = filename.split("/")[-1].split("\\")[-1]
        base = re.sub(r"\.[^.]+$", "", base)         # remove extension
        base = re.sub(r"[_\d]+", " ", base).strip()  # remove underscores/digits
        if base:
            return base.title()

    return "Candidate"

def extract_email(text: str) -> str:
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")
    return m.group(0) if m else "—"

def extract_phone(text: str) -> str:
    m = re.search(r"(\+?\d{1,3}[- ]*)?(\d[ -]?){9,12}\d", text or "")
    return m.group(0).strip() if m else "—"

def extract_linkedin(text: str) -> str:
    m = re.search(r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9_/.\-]+", text or "", re.IGNORECASE)
    return m.group(0) if m else "—"

def extract_github(text: str) -> str:
    m = re.search(r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_/.\-]+", text or "", re.IGNORECASE)
    return m.group(0) if m else "—"
