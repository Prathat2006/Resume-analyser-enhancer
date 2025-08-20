from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from llminit import LLMManager
from backend.resloader import lang_pdfreader
import yaml

# Define structured schema
class ResumeData(BaseModel):
    name: str = Field(default="", description="Candidate's full name")
    skills: list[str] = Field(default_factory=list, description="List of skills")
    education: str = Field(default="", description="Educational background")
    experience: str = Field(default="", description="Work experience summary")
    linkedin_profile: str = Field(default="", description="LinkedIn profile URL")
    github_profile: str = Field(default="", description="GitHub profile URL")
    projects: list[str] = Field(default_factory=list, description="List of projects")
    about: str = Field(default="", description="Short about section")
    other: str = Field(default="", description="Other relevant information")


def resume_extractor(file_path: str) -> ResumeData:
    # Parser
    parser = PydanticOutputParser(pydantic_object=ResumeData)

    # Load system prompt
    with open("sys_prompt.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)

    documents = lang_pdfreader(file_path)
    manager = LLMManager()
    llm_instances = manager.setup_llm_with_fallback()

    # Build prompt (merge sys_prompt with format instructions)
    sys_prompt = yaml_data["prompt"]
    prompt = PromptTemplate(
        template=sys_prompt + "\n\n{format_instructions}",
        input_variables=["resume_content"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Invoke LLM
    print("---" * 40)
    raw_response = manager.invoke_with_fallback(
        llm_instances,
        manager.DEFAULT_FALLBACK_ORDER,
        prompt.format(resume_content=documents[0].page_content),
    )

    # Parse response into structured object
    try:
        structured_response = parser.parse(raw_response)
        return structured_response.model_dump_json(indent=2) # JSON output
    except Exception as e:
        
        return raw_response

