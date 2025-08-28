import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# Import your backend modules
from backend.resume_praserer import resume_extractor
from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer
from backend.embedding_scorere import final_candidate_score

app = FastAPI()
# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] if using Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Directory to save resumes
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/evaluate")
async def evaluate_candidate(
    file: UploadFile, 
    url: str = Form(...)
):
    # Step 1: Save uploaded resume
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 2: Extract resume data
    resume_data = resume_extractor(file_path)

    # Step 3: Fetch + structure job data
    job_data = structurer(scrape_job_selenium(url))

    # Step 4: Get final candidate score (already JSON)
    score_result = final_candidate_score(job_data, resume_data)

    # Step 5: Return only the score_result JSON
    return JSONResponse(content=score_result)
