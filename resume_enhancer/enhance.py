from llminit import LLMManager
from backend.embedding_scorere import final_candidate_score  # your scorer
import json
from backend.resume_praserer import resume_extractor_from_text
# LLM setup
manager = LLMManager()
llm_instance = manager.setup_llm_with_fallback()

# Prompt template
prompt_template = """
You are a professional resume writer.
Enhance the given resume so it matches the job description while staying truthful.

Guidelines:
- Add missing but relevant keywords (if the candidate already has that skill but phrased differently).
- Rewrite work experience with strong action verbs.
- Keep achievements measurable and ATS-friendly.
- Do NOT invent fake experiences.
- All relevant information must be included like LinkedIn, GitHub, Email , location , contact etc.
JOB DESCRIPTION (JSON):
{job_json}

ORIGINAL RESUME:
{resume_content}

ENHANCED RESUME:
"""

def enhance_resume(job_json: dict, resume_content: str,resume_json: dict):
    # Step 1: Score before enhancement
    baseline_score = final_candidate_score(job_json, resume_json)

    # Step 2: Enhance resume with LLM
    prompt = prompt_template.format(
        job_json=json.dumps(job_json, indent=2),
        resume_content=resume_content
    )
    enhanced = manager.invoke_with_fallback(llm_instance, manager.DEFAULT_FALLBACK_ORDER, prompt)
    enhanced_resume = resume_extractor_from_text(enhanced)
    # Step 3: Score after enhancement
    new_score = final_candidate_score(job_json, enhanced_resume)

    # Step 4: Return results
    return {
        "baseline_score": baseline_score,
        "new_score": new_score,
        "enhanced_resume": enhanced_resume
    },enhanced
