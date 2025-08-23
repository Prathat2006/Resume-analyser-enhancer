from llminit import LLMManager
from backend.json_breaker import extract_experience , extract_education
from pydantic import BaseModel,Field 

manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()

# Define structured output model
class Eligibility(BaseModel):
    eligible: bool = Field(
        default=False,
        description="Is the candidate eligible for the job based on experience and education"
    )

# Prompt template for eligibility check
prompt_template = """
You are a strict job eligibility checker. 
Compare the candidate's qualifications with the job requirements.

Job Requirement:
Experience: {job_experience} years
Education: {job_education}

Candidate Profile:
Experience: {candidate_experience} years
Education: {candidate_education}

Rules:
1. Candidate must have at least the required years of experience.
2. Candidate's education must be equal to or higher than the required education level.
3. If both conditions are satisfied, return True. 
4. If either experience OR education fails, return False.

Return only True or False.
"""

def check_eligibility(candidate_experience, candidate_education, job_experience, job_education):
    try:
        # Prepare prompt for LLM
        prompt = prompt_template.format(
            candidate_experience=candidate_experience,
            candidate_education=candidate_education,
            job_experience=job_experience,
            job_education=job_education
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
    
def education_exp_importer(job,resume):
    reqexp=extract_experience(job)
    exp=extract_experience(resume)
    reqedu=extract_education(job)
    edu=extract_education(resume)