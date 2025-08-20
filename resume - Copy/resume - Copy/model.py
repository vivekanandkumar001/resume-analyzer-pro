# ===========================
# model.py
# Helpers for cleaning & predict
# ===========================
import re
import pickle
import nltk
from nltk.corpus import stopwords

# Download once
nltk.download('stopwords', quiet=True)
STOP = set(stopwords.words('english'))

# Lazy singletons
_EMBEDDER = None
_MODEL = None
_ENCODER = None

def _load_artifacts():
    global _EMBEDDER, _MODEL, _ENCODER
    if _EMBEDDER is None:
        _EMBEDDER = pickle.load(open("vectorizer.pkl", "rb"))
    if _MODEL is None:
        _MODEL = pickle.load(open("model.pkl", "rb"))
    if _ENCODER is None:
        _ENCODER = pickle.load(open("encoder.pkl", "rb"))
    return _EMBEDDER, _MODEL, _ENCODER

def clean_resume(txt: str) -> str:
    if not txt:
        return ""
    t = re.sub(r"http\S+|www\S+|https\S+|\S+@\S+", " ", txt)
    t = re.sub(r"<.*?>", " ", t)
    t = re.sub(r"[\r\n]+", " ", t)
    t = re.sub(r"[^a-zA-Z0-9 ]", " ", t)
    t = t.lower()
    t = " ".join(w for w in t.split() if w not in STOP)
    return t

def predict_category_and_conf(raw_text: str):
    """Return (category_name, confidence_percent_float)."""
    emb, model, enc = _load_artifacts()
    cleaned = clean_resume(raw_text)
    X = emb.encode([cleaned])
    prob = model.predict_proba(X)[0]
    idx = prob.argmax()
    cat = enc.inverse_transform([idx])[0]
    conf = float(prob[idx] * 100.0)
    return cat, conf
