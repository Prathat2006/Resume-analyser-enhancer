from pydantic import BaseModel, Field 
from typing import List, Optional
from llminit import LLMManager
import json
import re 

# Define schema with Pydantic
class JobPosting(BaseModel):
    title: str
    company: Optional[str]
    location: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    must_skills: List[str] = Field(default_factory=list)
    key_skills: List[str] = Field(default_factory=list)
    description: Optional[str]
    others: Optional[str]

def clean_json(raw: str) -> str:
    # Remove ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.DOTALL)
    return cleaned.strip()


# Initialize LLM manager
manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()

def structurer(job_data: dict) -> JobPosting:
        # Strict schema prompt
    prompt = f"""
    You are given a job posting extracted as JSON:

    {job_data}

    Return only valid JSON that matches this schema:

    {{
        "title": "string",
        "company": "string or null",
        "location": "string or null",
        "experience": "string or null",
        "education": "string or null",
        "must_skills": ["list of strings"],
        "key_skills": ["list of strings"],
        "description": "string or null",
        "others": "string or null"
    }}

    Ensure response is **valid JSON only** (no extra commentary).
    """

    # Invoke LLM
    response = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt, output_model=JobPosting)



    return response.model_dump_json(indent=2)