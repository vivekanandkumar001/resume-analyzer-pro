import os
import pickle
import numpy as np
import torch
import torch.nn as nn

POLICY_PATH = "rl_policy.pth"
METADATA_PATH = "rl_policy_metadata.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

class ResumePolicyNet(nn.Module):
    def __init__(self, resume_dim: int, role_count: int, role_embed_dim: int, hidden: int, action_count: int):
        super().__init__()
        self.role_emb = nn.Embedding(role_count, role_embed_dim)
        input_dim = (resume_dim if resume_dim > 0 else 0) + role_embed_dim
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.LayerNorm(hidden),
            nn.Linear(hidden, hidden // 2),
            nn.ReLU(),
            nn.Linear(hidden // 2, action_count)
        )

    def forward(self, resume_vec, role_idx):
        role_e = self.role_emb(role_idx)
        if resume_vec is None:
            x = role_e
        else:
            x = torch.cat([resume_vec, role_e], dim=-1)
        logits = self.net(x)
        return logits

def load_policy():
    if not (os.path.exists(POLICY_PATH) and os.path.exists(METADATA_PATH) and os.path.exists(VECTORIZER_PATH)):
        raise FileNotFoundError("RL policy or metadata/embedder not found.")
    meta = pickle.load(open(METADATA_PATH, "rb"))
    policy = ResumePolicyNet(
        resume_dim=meta["embed_dim"],
        role_count=len(meta["role_list"]),
        role_embed_dim=meta["role_embed_dim"],
        hidden=meta["hidden"],
        action_count=len(meta["skill_list"]),
    )
    policy.load_state_dict(torch.load(POLICY_PATH, map_location="cpu"))
    policy.eval()
    embedder = pickle.load(open(VECTORIZER_PATH, "rb"))
    return meta, policy, embedder

def score_skills_with_policy(policy, embedder, meta, resume_text: str, role: str):
    # Returns list of (skill, score) sorted desc
    role_list = meta["role_list"]
    skill_list = meta["skill_list"]
    role_idx = role_list.index(role) if role in role_list else 0

    if meta["embed_dim"] > 0 and resume_text:
        vec = embedder.encode([resume_text])[0]
        resume_tensor = torch.tensor(vec, dtype=torch.float32).unsqueeze(0)
    else:
        resume_tensor = None
    ridx = torch.tensor([role_idx], dtype=torch.long)
    with torch.no_grad():
        logits = policy(resume_tensor, ridx)
        probs = torch.softmax(logits, dim=-1).cpu().numpy().reshape(-1)
    ranked_idx = np.argsort(probs)[::-1]
    return [(skill_list[i], float(probs[i])) for i in ranked_idx]
