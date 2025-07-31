# ===========================
# model.py
# Uses BERT (sentence-transformers) 
# ===========================

import pandas as pd
import re
import nltk
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer

# Download stopwords
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# Load Dataset
df = pd.read_csv("UpdatedResumeDataSet.csv")
df = df[df['Category'].str.lower() != 'unknown']  # Remove unknowns

# Clean resume text
def clean_resume(txt):
    txt = re.sub(r"http\S+|www\S+|https\S+", '', txt)
    txt = re.sub(r"\S+@\S+", '', txt)
    txt = re.sub(r"<.*?>", '', txt)
    txt = re.sub(r"[\r\n]+", ' ', txt)
    txt = txt.lower()
    txt = ' '.join([word for word in txt.split() if word not in stop_words])
    return txt

df["cleaned_resume"] = df["Resume"].apply(clean_resume)

# Encode labels
y = df["Category"]
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# BERT-based embedding
model_name = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model_name)
X = embedder.encode(df["cleaned_resume"].tolist(), show_progress_bar=True)

# Balance dataset using SMOTE
smote = SMOTE(random_state=42)
X_bal, y_bal = smote.fit_resample(X, y_encoded)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=3000, class_weight='balanced')
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"\n✅ BERT Model Accuracy: {accuracy*100:.2f}%")

# Save model artifacts
pickle.dump(embedder, open("vectorizer.pkl", "wb"))  # Embedding model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(encoder, open("encoder.pkl", "wb"))
print("✅ Model, encoder, and BERT vectorizer saved!")
