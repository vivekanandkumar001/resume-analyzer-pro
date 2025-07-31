# ===========================
# Updated app.py for BERT-based model
# ===========================

import streamlit as st
import pickle
import re
import nltk
import pdfplumber
from docx import Document
from nltk.corpus import stopwords

# =======================
# Download stopwords
# =======================
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# =======================
# Load Resources
# =======================
@st.cache_resource
def load_resources():
    try:
        vectorizer = pickle.load(open("vectorizer.pkl", "rb"))  # SentenceTransformer
        model = pickle.load(open("model.pkl", "rb"))
        encoder = pickle.load(open("encoder.pkl", "rb"))
        return vectorizer, model, encoder
    except Exception as e:
        st.error(f"❌ Error loading model resources: {e}")
        return None, None, None

# =======================
# Text Extraction
# =======================
def extract_text(file, file_type):
    try:
        if file_type == 'pdf':
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        elif file_type == 'docx':
            doc = Document(file)
            return '\n'.join([para.text for para in doc.paragraphs])
        elif file_type == 'txt':
            return file.read().decode('utf-8', errors='ignore')
        return ''
    except Exception as e:
        st.error(f"❌ Error extracting text: {e}")
        return ''

# =======================
# Resume Cleaning
# =======================
def clean_resume(txt):
    txt = re.sub(r"http\S+|www\S+|https\S+", '', txt)
    txt = re.sub(r"\S+@\S+", '', txt)
    txt = re.sub(r"<.*?>", '', txt)
    txt = re.sub(r"[\r\n]+", ' ', txt)
    txt = txt.lower()
    txt = ' '.join([word for word in txt.split() if word not in stop_words])
    return txt

# =======================
# Main App
# =======================
def main():
    st.title("📄 Resume Screening App")
    st.write("Upload your resume (.pdf, .docx, or .txt) to predict the job category.")

    upload_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if upload_file:
        file_type = upload_file.name.split('.')[-1]
        resume_text = extract_text(upload_file, file_type)

        if not resume_text.strip():
            st.warning("⚠️ Could not extract readable text from the uploaded file.")
            return

        cleaned_resume = clean_resume(resume_text)

        vectorizer, model, encoder = load_resources()
        if not all([vectorizer, model, encoder]):
            return

        try:
            # Use BERT encode method
            vectorized_resume = vectorizer.encode([cleaned_resume])
        except Exception as e:
            st.error(f"❌ Error during vectorization: {e}")
            return

        if hasattr(model, "predict_proba"):
            try:
                probas = model.predict_proba(vectorized_resume)[0]
                top_n = 3
                top_indices = probas.argsort()[-top_n:][::-1]

                st.markdown("### 🎯 Top Matching Categories:")

                for i, idx in enumerate(top_indices):
                    category = encoder.inverse_transform([idx])[0]
                    confidence = probas[idx] * 100
                    emoji = "✅" if i == 0 else "🔹"
                    st.write(f"{emoji} **{category}** — {confidence:.2f}%")

                if probas[top_indices[0]] < 0.4:
                    st.warning("⚠️ Low confidence in top prediction — resume may be too generic or unmatched.")

            except Exception as e:
                st.error(f"❌ Error during prediction: {e}")
        else:
            prediction_index = model.predict(vectorized_resume)[0]
            category_name = encoder.inverse_transform([prediction_index])[0]
            st.success(f"✅ Predicted Category: **{category_name}**")
            st.info("Confidence score not available (model does not support `predict_proba`).")

if __name__ == "__main__":
    main()
