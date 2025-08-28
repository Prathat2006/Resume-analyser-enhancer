from typing import List
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llminit import LLMManager
from typing import Union

# 1. Define Pydantic models for structured output
class Personal(BaseModel):
    name: str
    about: str

class Contact(BaseModel):
    email: str
    phone: str
    location: str
    github: str
    linkedin: str

class Education(BaseModel):
    course: str
    institution: str
    location: str
    start_date: str
    end_date: str

class Experience(BaseModel):
    title: str
    company: str
    location: str
    start_date: str
    end_date: str
    description: List[str]

class SkillCategory(BaseModel):
    title: str
    elements: List[str]

class Project(BaseModel):
    title: str
    description: str
    link: str

class Resume(BaseModel):
    education: List[Education]
    experience: List[Experience]
    skills: List[SkillCategory]
    projects: List[Project]
    personal: List[Personal]
    contact: List[Contact]

def format_resume(resume_text):    
    manager = LLMManager()
    llm_instances = manager.setup_llm_with_fallback()    
    # 4. Prompt template
    spromtp="""
You are a resume parser AI.
Extract structured information from the given resume text.

Resume Text:
{resume_text}

Return the output in the required structured format.          
    """

    prompt = PromptTemplate(
        template=spromtp,
        input_variables=["resume_text"],
    )


    # Example usage
    # resume_text = r"""
    # {\n  "name": "AGASTHYA\u202fOMKUMAR",\n  "skills": [\n    "Search Engine Marketing (SEM)",\n    "Pay‑Per‑Click (PPC)",\n    "Google Ads",\n    "Google Analytics",\n    "SEO",\n    "Email Marketing",\n    "Social Media Marketing",\n    "Online Marketing",\n    "Marketing Operations",\n    "Campaign Management",\n    "Marketing Management",\n    "Business Development",\n    "Sales Enablement",\n    "Marketing analytics",\n    "A/B testing",\n    "Performance dashboards",\n    "Data‑fusion",\n    "Metric tracking",\n    "ROI analysis",\n    "Audience segmentation",\n    "Python",\n    "SQL",\n    "R",\n    "MATLAB",\n    "C#",\n    "pandas",\n    "NumPy",\n    "scikit‑learn",\n    "TensorFlow",\n    "PyTorch",\n    "Flask",\n    "Streamlit",\n    "Tableau",\n    "Power\u202fBI",\n    "Google Data Studio",\n    "Azure",\n    "AWS",\n    "Git",\n    "Docker",\n    "Linux",\n    "Advanced Excel"\n  ],\n  "education": "M.Sc. – Applied Mathematics (CGPA 8.26) from Defence Institute of Advanced Technology (2022‑2024); B.E. – Mechanical Engineering (CGPA 8.34) from BNM Institute of Technology (VTU) (2017‑2021)",\n  "experience": "Project Trainee – CAIR, DRDO (Aug\u202f2023\u202f–\u202fMar\u202f2024); Intern – Cognizant Technology Solutions (Mar\u202f2021\u202f–\u202fSept\u202f2021); 1+ year of hands‑on experience building data‑driven solutions for UAV surveillance, finance, and HR analytics.",\n  "linkedin_profile": "https://linkedin.com/in/agasthya-omkumar",\n  "github_profile": "https://github.com/AGasthya283",\n  "projects": [\n    "Fund‑Trail Analysis Platform (Flask web app with Hidden Markov Models and CTGAN)",\n    "HR Attrition Analytics (IBM HR Dataset)",\n    "Sign‑Language Recognition System (LRCN model with Streamlit UI)",\n    "UAV‑Based Maritime Multi‑Object Tracking (YOLO, transformers, Kalman filters, Streamlit GUI)"\n  ],\n  "about": "Analytical professional with a Master’s in Applied Mathematics and 1+ year experience building data‑driven solutions, skilled in digital‑marketing campaign management, SEM, PPC, marketing analytics, and end‑to‑end data pipeline development.",\n  "other": "Head Volunteer – ICDMAI 2023; Team Lead – KAVACH Cybersecurity Hackathon (Top‑5/3900 teams); Founder – Robotics Club at BNM Institute of Technology; 30+ GitHub repositories; Languages: English (professional), Hindi (native)."\n}'}
    # """

    response=manager.invoke_with_fallback(llm_instances,manager.DEFAULT_FALLBACK_ORDER,prompt.format(resume_text=resume_text),output_model=Resume)
    # print(response)
    return response.model_dump_json(indent=2)
# print(response.education[0].course)   # Example access
