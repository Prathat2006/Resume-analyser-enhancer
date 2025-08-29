from llminit import LLMManager
from backend.json_breaker import extract_experience , extract_education , extract_key_skills,extract_skills,extract_must_skills
from pydantic import BaseModel,Field 
import json
from typing import Dict, List, Tuple
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from configobj import ConfigObj

import time
manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()
config = ConfigObj('config.ini')   
current_time = int(time.time())
current_date = time.strftime("%Y-%m-%d", time.localtime(current_time))
# Define structured output model
class Eligibility(BaseModel):
    eligible: bool = Field(
        default=False,
        description="Is the candidate eligible for the job based on experience and education"
    )

# Prompt template for eligibility check
prompt_template = """You are a strict job eligibility checker.
Compare the candidate's qualifications with the job requirements.
Current date is {today} for extracting user experience.

Job Requirement:
Experience: {job_experience} years (if in a range like "0-1", take the lower bound for comparison)
Education: {job_education}

Candidate Profile:
Experience: {candidate_experience} (if given in months, convert to years and consider any nonzero month value as eligible for at least 0 years)
Education: {candidate_education}

Rules:

1.Candidate must have at least the required years of experience (treat months > 0 as meeting the minimum if requirement is 0 or range lower bound is 0).
2.Candidate's education must be equal to or higher than the required education level.
3.If both conditions are satisfied, return True.
4.If either experience OR education fails, return False.

Return only True or False.
"""

def check_eligibility(candidate_experience, candidate_education, job_experience, job_education):
    try:
        # Prepare prompt for LLM
        prompt = prompt_template.format(
            candidate_experience=candidate_experience,
            candidate_education=candidate_education,
            job_experience=job_experience,
            job_education=job_education,
            today=current_date
        )

        # Call LLM with structured output
        response = manager.invoke_with_fallback(
            llm_instances,
            manager.DEFAULT_FALLBACK_ORDER,
            prompt,
            output_model=Eligibility
        )

        # Return the eligibility boolean
        return response.eligible

    except Exception as e:
        print(f"Error checking eligibility: {e}")
        return False
    
# def education_exp_importer(job,resume):
#     reqexp=extract_experience(job)
#     exp=extract_experience(resume)
#     reqedu=extract_education(job)
#     edu=extract_education(resume)



# Load Qwen embedding model
cfg=config['embedding_model']
MODEL_NAME = cfg.get('embedding_model')
print(MODEL_NAME)
_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = AutoModel.from_pretrained(MODEL_NAME)

def embed_texts(texts: List[str]) -> np.ndarray:
    """Embed a list of texts with Qwen embedding model, return L2-normalized vectors."""
    if not texts:
        return np.zeros((0, 1536), dtype=np.float32)  # dim ~1536 for Qwen embedding
    encoded = _tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = _model(**encoded)
        # mean pooling
        emb = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    # normalize
    emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
    return emb.astype(np.float32)

def cosine_sim_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    if A.size == 0 or B.size == 0:
        return np.zeros((A.shape[0], B.shape[0]), dtype=np.float32)
    return np.matmul(A, B.T)
cfs=config['SIM_THRESHOLD']
SIM_THRESHOLD = cfs.get('skill_words_strictness', 0.8)
SIM_THRESHOLD=float(SIM_THRESHOLD)
# print(SIM_THRESHOLD)
# print(type(SIM_THRESHOLD))

def score_skills(job_skills: Dict[str, List[str]], resume_skills: Dict[str, List[str]]) -> Tuple[float, Dict]:
    must_skills = job_skills.get("must_skills", [])
    key_skills = job_skills.get("key_skills", [])
    resume = resume_skills.get("skills", [])

    # embeddings
    must_emb = embed_texts(must_skills)
    key_emb = embed_texts(key_skills)
    res_emb = embed_texts(resume)

    # similarity matrices
    must_sims = cosine_sim_matrix(must_emb, res_emb)
    key_sims = cosine_sim_matrix(key_emb, res_emb)

    must_best = must_sims.max(axis=1) if must_sims.size else np.array([])
    key_best = key_sims.max(axis=1) if key_sims.size else np.array([])

    # apply threshold: ignore weak matches
    must_best = np.where(must_best >= SIM_THRESHOLD, must_best, 0.0)
    key_best = np.where(key_best >= SIM_THRESHOLD, key_best, 0.0)

    MUST_W, KEY_W = 3.0, 1.0
    weighted_sum = MUST_W * must_best.sum() + KEY_W * key_best.sum()
    total_weight = MUST_W * len(must_best) + KEY_W * len(key_best)

    score_65 = 65.0 * (weighted_sum / total_weight) if total_weight > 0 else 0.0
    score_65 = float(max(0.0, min(65.0, score_65)))

    # breakdown with threshold check
    def _pairings(job_list, sim_mat):
        out = []
        if sim_mat.size == 0: return out
        best_idx = sim_mat.argmax(axis=1)
        best_val = sim_mat.max(axis=1)
        for i, j in enumerate(best_idx):
            sim = float(best_val[i])
            out.append({
                "job_skill": job_list[i],
                "best_resume_skill": resume[j] if sim >= SIM_THRESHOLD else None,
                "similarity": sim if sim >= SIM_THRESHOLD else 0.0
            })
        return out

    debug = {
        "score_out_of_65": score_65,
        "must_matches": _pairings(must_skills, must_sims),
        "key_matches": _pairings(key_skills, key_sims),
    }
    return score_65, debug


def final_candidate_score(job: dict, resume: dict) -> dict:
    """
    Evaluate candidate against job.
    Returns a dict with final score (0–100) and debug breakdown.
    """

    # Extract fields using provided extractors
    resume_Skills = extract_skills(resume)
    mustskill = extract_must_skills(job)  # assuming this returns {"must_skills": [...]}
    keyskill = extract_key_skills(job)       # assuming this returns {"key_skills": [...]}
    jobskill = {**mustskill, **keyskill}

    reqexp = extract_experience(job)
    exp = extract_experience(resume)
    reqedu = extract_education(job)
    edu = extract_education(resume)

    # Step 1: eligibility check
    eligible = check_eligibility(exp, edu, reqexp, reqedu)
    print(eligible)
    if not eligible:
        return {
            "final_score": 0.0,
            "eligible": False,
            "reason": "Candidate did not meet minimum experience/education requirements."
        }

    # Step 2: skills scoring (out of 65)
    score_65, debug = score_skills(jobskill, resume_Skills)

    # Step 3: final score
    final_score = 35.0 + score_65
    final_score = float(min(100.0, final_score))  # cap at 100
    final_score = round(final_score, 2)
    return {
        "final_score": final_score,
        "eligible": True,
        # "base_score": 35.0,
        # "skill_score": score_65,
        # "debug": debug
    }
