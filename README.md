# 🧠 Resume Insight AI

An intelligent, BERT-powered resume screening app built with Streamlit. It predicts the top 3 job categories for any uploaded resume and provides personalized improvement suggestions to boost resume relevance.

---

## 🚀 Features

- 📄 Upload resumes in `.pdf`, `.docx`, or `.txt` format
- 🤖 Uses BERT (`all-MiniLM-L6-v2`) for semantic understanding of resumes
- 🎯 Predicts top 3 most relevant job categories
- 📊 Shows confidence score for each prediction
- 🛠️ Gives suggestions to improve resume if confidence is low
- ✅ Simple, user-friendly Streamlit interface

---

## 📂 Project Structure

resume-insight-ai/
│
├── app.py                   # Streamlit app for uploading and predicting resumes
├── model.py                 # Script for training model using BERT embeddings
├── UpdatedResumeDataSet.csv # Labeled resume data (text + category)
│
├── model.pkl                # Trained Logistic Regression model
├── vectorizer.pkl           # BERT model (SentenceTransformer: all-MiniLM-L6-v2)
├── encoder.pkl              # LabelEncoder for job categories
│
├── requirements.txt         # Python dependencies
├── README.md                # Project overview and instructions
├── .gitattributes           # Git LFS tracking for large files (.pkl)
└── .gitignore               # Optional: ignores venv, .pkl, etc. in commits
