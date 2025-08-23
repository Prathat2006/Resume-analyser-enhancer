
# Example usage
if __name__ == "__main__":
    # url = "https://www.naukri.com/job-listings-land-acquisition-manager-reliance-industries-ril-navi-mumbai-8-to-13-years-190825020010?src=companyPageJobsDesk&sid=17556811513066580&xp=1&px=1"
    url = "https://www.naukri.com/job-listings-data-architect-tata-consultancy-services-hyderabad-pune-delhi-ncr-10-to-16-years-120825020348?src=companyPageJobsDesk&sid=17556814837582736&xp=1&px=1"
    details = scrape_job_selenium(url)
    print(details)
