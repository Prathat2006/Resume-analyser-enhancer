import requests
from bs4 import BeautifulSoup

url = "https://www.naukri.com/job-listings-customer-support-executive-randstad-ratnagiri-wardha-akola-1-to-3-years-250725018044?src=seo_srp&sid=1755672583185382&xp=1&px=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

job = {}

# Job Title
title = soup.find("h1", {"class": "jd-header-title"})
job["Job Title"] = title.get_text(strip=True) if title else "Not Found"

# Experience
exp = soup.find("span", {"class": "exp"})
job["Experience Required"] = exp.get_text(strip=True) if exp else "Not Found"

# Salary / Package
package = soup.find("span", {"class": "salary"})
job["Package"] = package.get_text(strip=True) if package else "Not Found"

# Role / Education
role = soup.find("div", {"class": "other-details"})
job["Role/Education"] = role.get_text(" ", strip=True) if role else "Not Found"

# Skills
skills = soup.find_all("a", {"class": "chip"})
job["Skills Required"] = [s.get_text(strip=True) for s in skills] if skills else []

# Job Description
desc = soup.find("div", {"class": "dang-inner-html"})
job["Job Description"] = desc.get_text(" ", strip=True) if desc else "Not Found"

print(job)
