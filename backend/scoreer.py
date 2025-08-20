from llminit import LLMManager
from langchain.prompts import PromptTemplate
import json

manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()

resume_json = {
  "name": "AGASTHYA OMKUMAR",
  "skills": [
    "Machine Learning",
    "Computer Vision",
    "Image Processing",
    "OCR",
    "NLP",
    "Time Series",
    "Image Recognition",
    "Multi-Object Tracking",
    "Spatial Data Analysis",
    "GenAI",
    "LLMs",
    "Mathematical Modelling",
    "Azure",
    "AWS",
    "Latex",
    "Python",
    "Matlab",
    "SQL",
    "R",
    "C#"
  ],
  "experience": "Project Trainee Aug 2023 - Mar 2024 at CAIR-DRDO Bengaluru, KA\n• Conducted Research on UAV based Multi Object Tracking in Maritime Domain for Surveillance and Search & Rescue Operations.\n• Developed tracking models for specific use-cases with high accuracy, tackling problems like Occlusion and Re-Identification using Sensor Data and Image Recognition Techniques respectively.\n• Developed Data Fusion Models for Visual and Sensor Data to tackle Occlusion and Re-Identification challenges.\n• Visualized Model performance and metrics using frameworks like Streamlit.\n• Trained Models on Stand alone GPU systems and Edge Computing Technology.",
  "linkedin_profile": "https://linkedin.com/in/agasthya-omkumar",
  "github_profile": "https://github.com/AGasthya283",
  "projects": [
    "UAV-based Maritime Multi-Object Tracking.Masters Thesis Project.",
    "Research on Multi-Object Tracking methods with a focus on integrating Image Recognition techniques."
  ],
  "about": "Highly skilled ML Engineer with expertise in Machine Learning, Computer Vision and NLP. Leveraging research experience at CAIR-DRDO and advanced training I am now seeking Data Scientist or AI-related roles to drive impactful results in a dynamic organization.",
  "other": "Certified in AWS"
}

job_json ={
  "title": "Informatica Developer",
  "company": "Tata Consultancy Services Careers",
  "location": None,
  "experience": "1 year",
  "education": "Education UG: B.Tech/B.E. in Any Specialization",
  "skills": [
    "Powercenter",
    "Informatica Powercenter",
    "Oracle"
  ],
  "description": "Job description   Desired   Competencies (Technical/Behavioral Competency)   Must-Have Informatica   Powercenter, Oracle, Unix   Good-to-Have Knowledge of Unix shell scripting and CA7.   SN Responsibility of / Expectations from   the Role    1 Designing, developing and implementing mappings/ transformations in using Informatica Powercenter.   2 Good experience in using Oracle SQL PLSQL and Unix   3 Experience with Agile methodologies    4 Attention to detail, Desire and ability to work in a multi-distributed team environment   5 Ability to excel in a short timeframe under short sprints   6 Strong communication and presentation skills Role:  Business Analyst , Industry Type:  IT Services & Consulting , Department:  Data Science & Analytics , Employment Type:  Full Time, Permanent Role Category:  Business Intelligence & Analytics Education UG:  B.Tech/B.E. in Any Specialization read more Key Skills Skills highlighted with ‘ ’ are preferred keyskills Powercenter Informatica Powercenter Oracle"
}

prompt_template = PromptTemplate(
    input_variables=["resume_json", "job_json"],
    template="""
You are an expert HR recruiter. Your task is to evaluate how well a candidate's resume matches a job requirement.

You will be given two JSON objects:

**Resume JSON:**
{resume_json}

**Job Requirements JSON:**
{job_json}

### Scoring Rules:
1. Education + Experience (combined, max 35 points)
   - If candidate's education level is greater than or equal to required AND candidate's experience (in years) is greater than or equal to required → award 35 points.
   - If either education OR experience does not meet the requirement → award 0 points.

2. Skills (max 40 points)
   - If candidate has all required skills → 40 points.
   - If partially matches → proportional score based on % match.
   - If no match → 0 points.

3. Projects (max 25 points)
   - If candidate has projects directly relevant to the job role → 25 points.
   - If somewhat relevant → partial points.
   - If no relevant projects → 0 points.

### Output strictly in JSON:
{{
  "education_score": <number>,
  "experience_score": <number>,
  "skills_score": <number>,
  "projects_score": <number>,
  "total_score": <number>,
  "remarks": "<short reason of evaluation>"
}}
"""
)

# Format the prompt with actual data
formatted_prompt = prompt_template.format(
    resume_json=json.dumps(resume_json, indent=2),
    job_json=json.dumps(job_json, indent=2)
)

# Now invoke the LLM with the formatted prompt
response = manager.invoke_with_fallback(
    llm_instances,
    manager.DEFAULT_FALLBACK_ORDER,
    formatted_prompt,  # Use the formatted string, not the template object
)

# print(response)