from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_job_selenium(url: str) -> dict:
    options = Options()
    # options.add_argument("--headless")  # run in background
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    job = {
        "title": None,
        "company": None,
        "education": None,
        "experience": None,
        "key_skills": [],
        "description": None,
    }

    # --- Extract job title ---
    title_tag = soup.find("h1")
    if title_tag:
        job["title"] = title_tag.get_text(strip=True)

    # --- Company ---
    company_tag = soup.find('div', class_='styles_jd-header-comp-name__MvqAI')

    # Find the first 'a' tag within that div and get its 'title' attribute
    if company_tag:
        company_link = company_tag.find('a')
        if company_link:
            company_title = company_link.get('title')
            job["company"] = company_title
    # --- Experience ---
    exp_tag = soup.find("span", {"class": "styles_jhc__exp__k_giM"})
    if exp_tag:
        job["experience"] = exp_tag.get_text(strip=True)
    # --- Skills ---
    key_skills_div = soup.find('div', class_='styles_key-skill__GIPn_')
    if key_skills_div:
        for a_tag in key_skills_div.find_all('a'):
            span_tag = a_tag.find('span')
            if span_tag:
                job["key_skills"].append(span_tag.text.strip())


    # --- Education (often in "education" section) ---
    edu_section = soup.find("div", {"class": "styles_education__KXFkO"})
    if edu_section:
        job["education"] = edu_section.get_text(" ", strip=True)


    # --- Job Description ---
    desc_section = soup.find("section", {"class": "styles_job-desc-container__txpYf"})
    if desc_section:
        job["description"] = desc_section.get_text(" ")

    return job


# # Example usage
# if __name__ == "__main__":
#     # url = "https://www.naukri.com/job-listings-land-acquisition-manager-reliance-industries-ril-navi-mumbai-8-to-13-years-190825020010?src=companyPageJobsDesk&sid=17556811513066580&xp=1&px=1"
#     url = "https://www.naukri.com/job-listings-data-architect-tata-consultancy-services-hyderabad-pune-delhi-ncr-10-to-16-years-120825020348?src=companyPageJobsDesk&sid=17556814837582736&xp=1&px=1"
#     details = scrape_job_selenium(url)
#     print(details)
