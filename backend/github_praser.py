import requests
from bs4 import BeautifulSoup
# from langchain.prompts import PromptTemplate



# --- Step 1: Scrape GitHub Profile ---

def fetch_github_repos(url: str):
    # Ensure URL points to repositories tab
    if "?tab=repositories" not in url:
        url = url.rstrip("/") + "?tab=repositories"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch GitHub repositories")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract Repositories (names + links)
    repos = []
    repo_list = soup.find_all("a", {"itemprop": "name codeRepository"})
    for repo in repo_list:
        repo_name = repo.get_text(strip=True)
        repo_url = "https://github.com" + repo["href"]
        repos.append({"name": repo_name, "url": repo_url})
    
    return repos

# # --- Step 2: LLM Prompt ---
# prompt = PromptTemplate(
#     input_variables=["projects"],
#     template="""
# You are an assistant that summarizes GitHub repository information.

# Projects:
# {projects}

# Create a structured markdown summary:
# - List of Projects (name + url)
#     """
# )

# --- Step 3: LLM Chain ---
# response = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt.format(resume_content=documents[0].page_content))
# print(response)

# --- Step 4: Run ---
if __name__ == "__main__":
    github_url = "https://github.com/KumariKanchan734"   # replace with actual profile
    # about, repos = fetch_github_profile(github_url)
    print(fetch_github_repos(github_url))
    # Format repos for LLM
    # projects_str = "\n".join([f"- {r['name']}: {r['url']}" for r in repos])

    # result = manager.invoke_with_fallback(llm_instances, manager.DEFAULT_FALLBACK_ORDER, prompt.format(about=about, projects=projects_str))
    # print(result)
