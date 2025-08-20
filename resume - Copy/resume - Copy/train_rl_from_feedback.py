
# ==================================================
# train_rl_from_feedback.py - lightweight RL updates
# ==================================================
import csv
import json
import os

RL_WEIGHTS_FILE = "rl_weights.json"

def _load_weights():
    if os.path.exists(RL_WEIGHTS_FILE):
        try:
            return json.load(open(RL_WEIGHTS_FILE, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_weights(w):
    json.dump(w, open(RL_WEIGHTS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def train_incremental():
    """
    Reads positive/negative feedback and adjusts per-skill weights.
    Very simple rule:
      +1 reward on a (kind,text) that mentions a known skill -> +0.2
      -1 reward -> -0.2
    You can extend to projects/courses/certs as needed.
    """
    weights = _load_weights()

    def tick(path, delta):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                txt = (row.get("text") or "").lower()
                # crude tokenization: alnum tokens
                for token in txt.split():
                    t = "".join(ch for ch in token if ch.isalnum())
                    if not t:
                        continue
                    if 2 <= len(t) <= 20:
                        weights[t] = round(weights.get(t, 0.0) + delta, 4)

    # Use the filenames present in the project
    tick("feedback_positive.csv", +0.2)
    tick("feedback_negative.csv", -0.2)
    _save_weights(weights)
    return True

if __name__ == "__main__":
    train_incremental()
    print("RL weights updated.")
