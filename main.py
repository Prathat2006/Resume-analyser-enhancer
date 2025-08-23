# # from langchain_community.document_loaders import PyPDFLoader
# from backend.resume_praserer import resume_extractor

# resume=((resume_extractor("resume0.pdf")))

# from backend.naukridotcomfetcher import scrape_job_selenium
# from backend.jobdetailstructurer import structurer


# job=(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-data-science-engineer-persistent-pune-5-to-10-years-300725032355?src=companyPageJobsDesk&sid=17556979136603746&xp=2&px=1")))


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


from llminit import LLMManager

manager = LLMManager()
llm_instances = manager.setup_llm_with_fallback()

prompt="hi"
annu = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt)
print(annu)