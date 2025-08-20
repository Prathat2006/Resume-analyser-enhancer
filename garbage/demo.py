from naukridotcomfetcher import scrape_job_selenium
from jobdetailstructurer import structurer


def main():
    job_data = scrape_job_selenium("https://www.naukri.com/job-listings-informatica-developer-tata-consultancy-services-hyderabad-5-to-10-years-190825028172?src=companyPageJobsDesk&sid=17556946359356792&xp=2&px=1")

    structured_data = structurer(job_data)
    print(structured_data)

main()