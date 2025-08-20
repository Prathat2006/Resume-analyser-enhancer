# from langchain_community.document_loaders import PyPDFLoader
# from backend.resume_praserer import resume_extractor

# print(type(resume_extractor("resume0.pdf")))

from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer


print(type(structurer(scrape_job_selenium("https://www.naukri.com/job-listings-data-science-engineer-persistent-pune-5-to-10-years-300725032355?src=companyPageJobsDesk&sid=17556979136603746&xp=2&px=1"))))