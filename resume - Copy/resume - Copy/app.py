import streamlit as st
from extract_utils import extract_text_from_file, extract_name_from_text
from model import clean_resume, predict_category_and_conf
from suggest import analyze_for_role, ALL_ROLES

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    resume_text = extract_text_from_file(uploaded_file)
    if not resume_text:
        st.error("Couldn't read text from the file. Try another format.")
        st.stop()

    st.session_state["resume_text"] = resume_text

    # Extract candidate name
    name = extract_name_from_text(resume_text, uploaded_file.name)
    st.subheader(f"⏳ Hold On: **{name}**, I am analyzing your resume...")

    # Auto-predict category
    st.subheader("🔍 Auto-Detect Role Category")
    pred_category, confidence = predict_category_and_conf(resume_text)
    st.success(f"✅ Best Match Category: **{pred_category}**  (Confidence: {confidence:.2f}%)")

    # Let user choose category
    st.markdown("### 🎯 Choose Your Target Role / Category")
    roles = sorted(set(ALL_ROLES + [pred_category]))
    default_idx = roles.index(pred_category) if pred_category in roles else 0
    chosen_category = st.selectbox("Pick or confirm a category:", roles, index=default_idx)
    st.session_state["chosen_category"] = chosen_category

    # Analyze
    st.subheader("🧠 AI Suggestions for Your Resume")
    result = analyze_for_role(resume_text, chosen_category)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔧 Improvements")
        for it in result["improvements"]:
            st.write(f"- {it}") if result["improvements"] else st.write("Looks good!")

        st.markdown("#### 🧩 Missing / Important Skills")
        for s in result["missing_skills"]:
            st.write(f"- {s}") if result["missing_skills"] else st.write("No critical skill gaps found.")

    with col2:
        st.markdown("#### 💡 Projects to Add")
        for p in result["projects"]: st.write(f"- {p}")

        st.markdown("#### 🎓 Recommended Courses")
        for c in result["courses"]: st.write(f"- {c}")

        st.markdown("#### 🏅 Suggested Certificates")
        for c in result["certificates"]: st.write(f"- {c}")

    st.info("✏️ To edit the resume, open **Resume Editor** from the left sidebar.")
else:
    st.caption("Upload a resume to get started.")
