from llminit import LLMManager
from langchain.prompts import PromptTemplate
from backend.resloader import lang_pdfreader
manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()


def check_spelling(filepath):
    documents = lang_pdfreader(filepath)
    sprompt = """
    Rewrite the same content with correct spelling:
    {resume_content}
    *Note* : Only correct the spelling mistakes, do not change any other content.
    
    """
    prompt = PromptTemplate(
        template=sprompt,
        input_variables=["resume_content"],
    )
    resume_text = "\n".join([doc.page_content for doc in documents])
    raw_response = manager.invoke_with_fallback(
        llm_instances,
        manager.DEFAULT_FALLBACK_ORDER,
        prompt.format(resume_content=resume_text),
    )
    # output_model=ResumeData

    return raw_response