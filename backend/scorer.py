import json
from llminit import LLMManager

def score_resume(resume_data, job_details):
    """
    Scores a resume against job details using an LLM.

    Args:
        resume_data (dict): The structured data extracted from the resume.
        job_details (dict): The structured data extracted from the job posting.

    Returns:
        dict: A dictionary containing the score and analysis.
    """
    llm_manager = LLMManager()
    llm_instances = llm_manager.setup_llm_with_fallback()
    
    # Prepare the prompt for the LLM
    prompt = f"""
    You are an expert hiring manager. Your task is to analyze the provided resume and job description, and then calculate a compatibility score.

    Job Description:
    {json.dumps(job_details, indent=2)}

    Resume:
    {json.dumps(resume_data, indent=2)}

    Based on the comparison, provide a JSON output with the following keys:
    - "score": An overall compatibility score out of 100.
    - "summary": A brief summary of why the candidate is a good or bad fit.
    - "strengths": A list of key strengths of the candidate for this role.
    - "weaknesses": A list of areas where the candidate's profile is weak for this role.
    
    The score should be based on the alignment of skills, experience, and education.
    """
    
    # Use the LLM to get the analysis
    fallback_order = llm_manager.DEFAULT_FALLBACK_ORDER
    response_text = llm_manager.invoke_with_fallback(llm_instances, fallback_order, prompt)
    
    # Clean and parse the JSON response
    try:
        # The LLM might return the JSON within a code block
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        return json.loads(response_text)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing LLM response: {e}")
        return {
            "score": 0,
            "summary": "Could not generate a score. There was an issue with the analysis.",
            "strengths": [],
            "weaknesses": []
        }