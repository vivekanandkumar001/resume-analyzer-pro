import io
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document

from model import predict_category_and_conf
from suggest import analyze_for_role, ALL_ROLES, log_feedback_rows

# ✅ import all extractors
from extract_utils import (
    extract_name_from_text,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
)

st.set_page_config(page_title="Resume Editor", layout="wide")
st.title("✏️ Resume Editor")

if "resume_text" not in st.session_state:
    st.warning("Please upload and analyze a resume on the main page first.")
    st.stop()

resume_text = st.session_state["resume_text"]
chosen_category = st.session_state.get("chosen_category", ALL_ROLES[0])

# ----------------------------
# Auto-extracted basics
# ----------------------------
with st.expander("🔎 Auto-Extracted Basics (you can copy these into your resume):", expanded=True):
    nm = extract_name_from_text(resume_text)
    em = extract_email(resume_text)
    ph = extract_phone(resume_text)
    li = extract_linkedin(resume_text)
    gh = extract_github(resume_text)

    st.write(f"**Name (guess):** {nm}")
    st.write(f"**Email:** {em}")
    st.write(f"**Phone:** {ph}")
    st.write(f"**LinkedIn:** {li}")
    st.write(f"**GitHub:** {gh}")

# ----------------------------
# Editor
# ----------------------------
st.markdown("### 📝 Edit Your Resume Text")
edited_resume = st.text_area("Make your changes below:", value=resume_text, height=420)

st.markdown("### 🎯 Target Role / Category (override if you want)")
roles = sorted(set(ALL_ROLES + [chosen_category]))
cat_idx = roles.index(chosen_category) if chosen_category in roles else 0
user_category = st.selectbox("Category to analyze against:", roles, index=cat_idx)
st.session_state["chosen_category"] = user_category

if st.button("🔄 Re-check Edited Resume"):
    pred_cat, conf = predict_category_and_conf(edited_resume)
    st.success(f"Model thinks: **{pred_cat}** (Confidence: {conf:.2f}%)")
    res = analyze_for_role(edited_resume, user_category)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔧 Improvements")
        for it in res["improvements"]: st.write(f"- {it}") if res["improvements"] else st.write("Looks clean!")

        st.markdown("#### 🧩 Missing / Important Skills")
        for s in res["missing_skills"]: st.write(f"- {s}") if res["missing_skills"] else st.write("No gaps detected.")

    with col2:
        st.markdown("#### 💡 Projects to Add")
        for p in res["projects"]: st.write(f"- {p}")

        st.markdown("#### 🎓 Recommended Courses")
        for c in res["courses"]: st.write(f"- {c}")

        st.markdown("#### 🏅 Suggested Certificates")
        for c in res["certificates"]: st.write(f"- {c}")

    st.session_state["edited_resume"] = edited_resume
    st.session_state["last_analysis"] = res

# ----------------------------
# Download helpers
# ----------------------------
def make_pdf(text: str) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    left, top = 50, height - 50
    c.setFont("Helvetica", 11)
    y = top
    for line in (text or "").splitlines():
        while len(line) > 95:
            c.drawString(left, y, line[:95])
            line = line[95:]
            y -= 14
            if y < 60:
                c.showPage(); c.setFont("Helvetica", 11); y = top
        c.drawString(left, y, line)
        y -= 14
        if y < 60:
            c.showPage(); c.setFont("Helvetica", 11); y = top
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()

def make_docx(text: str) -> bytes:
    buf = io.BytesIO()
    d = Document()
    for para in (text or "").splitlines():
        d.add_paragraph(para)
    d.save(buf)
    buf.seek(0)
    return buf.read()

st.markdown("### ⬇️ Download Updated Resume")
target_text = st.session_state.get("edited_resume", resume_text)

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("📄 Download PDF", data=make_pdf(target_text), file_name="Updated_Resume.pdf", mime="application/pdf")
with c2:
    st.download_button("📝 Download DOCX", data=make_docx(target_text), file_name="Updated_Resume.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
with c3:
    st.download_button("📃 Download TXT", data=target_text.encode("utf-8"), file_name="Updated_Resume.txt", mime="text/plain")

# ----------------------------
# Feedback
# ----------------------------
st.markdown("### 📝 Feedback (helps the AI improve)")
fb_txt = st.text_input("Optional comments")
reward = st.radio("Were these suggestions useful?", [1, -1], index=0, format_func=lambda x: "👍 Yes" if x == 1 else "👎 No")
if st.button("Submit Feedback"):
    from train_rl_from_feedback import train_incremental
    analysis = st.session_state.get("last_analysis", analyze_for_role(target_text, user_category))
    rows = []
    for s in analysis.get("missing_skills", []): rows.append(("skill", s))
    for p in analysis.get("projects", []): rows.append(("project", p))
    for c in analysis.get("courses", []): rows.append(("course", c))
    for c in analysis.get("certificates", []): rows.append(("certificate", c))
    log_feedback_rows("session", user_category, rows, reward, fb_txt)
    st.success("✅ Feedback recorded.")
    try:
        train_incremental()
        st.caption("RL weights lightly updated.")
    except Exception:
        st.caption("Feedback logged.")
