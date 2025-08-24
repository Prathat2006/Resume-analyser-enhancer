# # from langchain_community.document_loaders import PyPDFLoader
from backend.resume_praserer import resume_extractor

resume=((resume_extractor("resume0.pdf")))

from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer


# job=(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-data-science-engineer-persistent-pune-5-to-10-years-300725032355?src=companyPageJobsDesk&sid=17556979136603746&xp=2&px=1")))
job=(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-data-architect-tata-consultancy-services-hyderabad-pune-delhi-ncr-10-to-16-years-120825020348?src=companyPageJobsDesk&sid=17556814837582736&xp=1&px=1")))
print(job)

# # from backend.github_praser import fetch_github_repos

# # print(fetch_github_repos("https://github.com/Prathat2006"))

# print(job)
# print("==="*40)
# print(resume)
# from backend.json_breaker import extract_experience ,extract_education
# from backend.embedding_scorere import check_eligibility

# print("==="*40)
# reqexp=extract_experience(job)
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
from backend.embedding_scorere import score_skills, final_candidate_score

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

print(final_candidate_score(job, resume))