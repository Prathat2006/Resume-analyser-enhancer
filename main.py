# from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate

from llminit import LLMManager
from resloader import lang_pdfreader
import yaml

with open("sys_prompt.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)


documents = lang_pdfreader("resume0.pdf")
manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()


sys_prompt = yaml_data["prompt"]
prompt = PromptTemplate(template=sys_prompt, input_variables=["resume_content"])

# Invoke LLM with fallback
print("----"*50)
response = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt.format(resume_content=documents[0].page_content))
print(response)