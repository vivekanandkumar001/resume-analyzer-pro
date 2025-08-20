import streamlit as st
from suggest import suggest_from_resume, ROLE_SKILLS
from extract_utils import (
    extract_name_from_text,
    extract_email,
    extract_phone,
)
import re

st.set_page_config(page_title="Resume Editor", layout="wide")

st.title("✍️ Resume Editor")

# ----------------------------
# Extra helpers
# ----------------------------
def extract_linkedin(text: str) -> str:
    match = re.search(r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9_/.\-]+", text or "", re.IGNORECASE)
    return match.group(0) if match else "—"

def extract_github(text: str) -> str:
    match = re.search(r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_/.\-]+", text or "", re.IGNORECASE)
    return match.group(0) if match else "—"

# ----------------------------
# Main
# ----------------------------
if "resume_text" not in st.session_state:
    st.warning("⚠️ Please upload and analyze a resume first in the Analyzer page.")
else:
    # Resume Editor
    resume_text = st.text_area("📝 Edit your Resume", st.session_state["resume_text"], height=400)
    st.session_state["resume_text"] = resume_text

    # 🔎 Auto-extract details
    name_guess = extract_name_from_text(resume_text)
    email_guess = extract_email(resume_text)
    phone_guess = extract_phone(resume_text)
    linkedin_guess = extract_linkedin(resume_text)
    github_guess = extract_github(resume_text)

    with st.expander("🔎 Auto-Extracted Basics (you can copy these into your resume):", expanded=True):
        st.write(f"**Name (guess):** {name_guess}")
        st.write(f"**Email:** {email_guess}")
        st.write(f"**Phone:** {phone_guess}")
        st.write(f"**LinkedIn:** {linkedin_guess}")
        st.write(f"**GitHub:** {github_guess}")

    # Choose Role Again
    st.subheader("🎯 Re-check against a Target Role")
    target_role = st.selectbox("Select category", list(ROLE_SKILLS.keys()))

    if st.button("Re-Analyze Edited Resume"):
        results = suggest_from_resume(resume_text, target_role)

        st.subheader("📌 Analysis on Edited Resume")
        if results.missing_skills:
            st.markdown("### 🚀 Missing Skills:")
            st.write(", ".join(results.missing_skills))

            st.markdown("### 💡 Suggested Projects:")
            for sug in results.suggestions:
                st.write(f"- {sug.project_title}")
        else:
            st.success("✅ Your edited resume already covers most required skills!")

    st.info("👉 After editing, you can also download your resume in different templates (to be added in next step).")
