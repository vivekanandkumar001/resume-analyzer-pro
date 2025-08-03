# ===========================
# editor.py — Engaging Resume Editor
# ===========================
import streamlit as st

def resume_editor(original_text: str):
    """
    Engaging editor with sections, live preview, and image upload.
    Returns (combined_resume_text, uploaded_image).
    """

    st.subheader("🎨 Resume Editing Panel")

    # Tabs for better experience
    tab1, tab2, tab3 = st.tabs(["📝 Edit Resume", "👀 Live Preview", "🖼 Profile Image"])

    # =======================
    # TAB 1 — Resume Editing
    # =======================
    with tab1:
        st.write("### ✏️ Update Your Resume Details")

        # Simple structured inputs
        name = st.text_input("Full Name")
        title = st.text_input("Professional Title")
        summary = st.text_area("Summary / Objective", height=100, value="")

        skills = st.text_area("Skills (comma separated)", height=80, value="")
        experience = st.text_area("Work Experience", height=150, value="")
        education = st.text_area("Education", height=120, value="")
        projects = st.text_area("Projects / Achievements", height=120, value="")

        # Combine all fields into one text block
        edited_text = f"""{name}\n{title}\n
Summary:\n{summary}\n
Skills:\n{skills}\n
Experience:\n{experience}\n
Education:\n{education}\n
Projects:\n{projects}
"""

    # =======================
    # TAB 2 — Live Preview
    # =======================
    with tab2:
        st.write("### 📄 Live Resume Preview")
        st.markdown("---")
        st.markdown(f"""
        **{name if name else "Your Name"}**  
        *{title if title else "Your Title"}*  

        **Summary**  
        {summary if summary else "Your summary will appear here..."}  

        **Skills**  
        {skills if skills else "Your skills will appear here..."}  

        **Experience**  
        {experience if experience else "Your experience will appear here..."}  

        **Education**  
        {education if education else "Your education will appear here..."}  

        **Projects**  
        {projects if projects else "Your projects will appear here..."}  
        """)
        st.markdown("---")

    # =======================
    # TAB 3 — Image Upload
    # =======================
    with tab3:
        uploaded_image = st.file_uploader("Upload profile image (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Profile Image", width=150)

    return edited_text, uploaded_image
