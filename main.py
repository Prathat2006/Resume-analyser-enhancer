# # # from langchain_community.document_loaders import PyPDFLoader
# from backend.resume_praserer import resume_extractor
# from backend.naukridotcomfetcher import scrape_job_selenium
# from backend.jobdetailstructurer import structurer
# from backend.embedding_scorere import final_candidate_score,check_eligibility
# from resume_enhancer.enhance import enhance_resume
# from backend.resloader import lang_pdfreader, read_pdf_to_text
# from resume_enhancer.src.build import generate_resume_from_json
# from resume_enhancer.formater import format_resume
import json
from llminit import LLMManager
from configobj import ConfigObj
print("import done")
manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()
prompt="hi"
order=ConfigObj('config.ini')["mode"]["order"]
response = manager.invoke_with_fallback(llm_instances,order,prompt)
print(response)
# resume=((resume_extractor(r"resume0.pdf")))
# print(resume)
# job=(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-data-science-engineer-persistent-pune-5-to-10-years-300725032355?src=companyPageJobsDesk&sid=17556979136603746&xp=2&px=1")))
# job=(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-campaign-management-new-associate-accenture-solutions-pvt-ltd-hyderabad-0-to-1-years-280725913582?src=seo_srp&sid=17563086863932737&xp=1&px=1")))
# print(job)
# print("==="*50)
# documents = lang_pdfreader("resume0.pdf")
# documents = read_pdf_to_text("resume0.pdf")
# print(documents)
# # # resume_text = "\n".join([doc.page_content for doc in documents])
# resume_text = documents
# score,resume_enhanced = enhance_resume(job, resume_text,resume)
# # print(score)
# # print("==="*40)
# # print(resume_enhanced)
# resume_text=resume_enhanced
# enhance_resume=format_resume(resume_text)
# # print(enhance_resume)
# # print(type(enhance_resume))
# resume_dict = json.loads(enhance_resume)

# # now pass dict instead of string
# generate_resume_from_json(resume_dict)

# print("backend done")

# print(final_candidate_score(job, resume))

# # # from backend.github_praser import fetch_github_repos

# # # print(fetch_github_repos("https://github.com/Prathat2006"))

# # print(job)
# # print("==="*40)
# # print(resume)
# # from backend.json_breaker import extract_experience ,extract_education
# # from backend.embedding_scorere import check_eligibility

# # print("==="*40)
# # reqexp=extract_experience(job)
# exp=extract_experience(resume)
# reqedu=extract_education(job)
# edu=extract_education(resume)


# print(reqedu)
# print(edu)

# print(reqexp)
# print(exp)
# print("==="*40)
# print(check_eligibility(reqexp["experience"], exp["experience"], reqedu["education"], edu["education"]))


# from llminit import LLMManager

# manager = LLMManager()
# llm_instances = manager.setup_llm_with_fallback()

# prompt="hi"
# annu = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt)
# print(annu)
# from backend.json_breaker import extract_skills, extract_key_skills, extract_must_skills


# job = {
#        "must_skills": ["Python", "Machine Learning"],
#        "key_skills": ["Pandas", "SQL", "NLP"]
#    }
# resume = {
#     "skills": ["Python", "SQL", "Deep Learning", "NLP"]
# }

# resume_Skills=extract_skills(resume)
# # print(resume_Skills)


# mustskill=extract_must_skills(job)
# keyskill=extract_key_skills(job)
# print(mustskill)
# print(keyskill)
# print("__"*50)
# jobskill={**mustskill,**keyskill}

# score, dbg = score_skills(jobskill, resume_Skills)
# print("Final Score:", score)
# print("Debug:", dbg)




# from backend.spelling_Check import check_spelling

# print(check_spelling("resume0.pdf"))