import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# Import your backend modules
from backend.resume_praserer import resume_extractor
from backend.naukridotcomfetcher import scrape_job_selenium
from backend.jobdetailstructurer import structurer
from backend.embedding_scorere import final_candidate_score
from resume_enhancer.enhance import enhance_resume
from resume_enhancer.formater import format_resume
from resume_enhancer.src.build import generate_resume_from_json
import json
# Add this at the top
from fastapi import BackgroundTasks
import uuid
from fastapi.responses import FileResponse
import os
# Store sessions in memory (can later replace with Redis/DB)
SESSIONS = {}


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
from fastapi import UploadFile, File, Form

@app.post("/evaluate")
async def evaluate_candidate(
    resume: UploadFile = File(...),   # match "resume"
    job_url: str = Form(...),        # match "job_url"
):
    # Step 1: Save uploaded resume
    file_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(file_path, "wb") as f:
        f.write(await resume.read())

    # Step 2: Extract resume data
    resume_data = resume_extractor(file_path)

    # Step 3: Fetch + structure job data
    job_data = structurer(scrape_job_selenium(job_url))

    # Step 4: Get candidate score
    score_result = final_candidate_score(job_data, resume_data)

    # Step 5: Generate a session_id
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "resume_data": resume_data,
        "job_data": job_data,
        "file_path": file_path
    }

    # Step 6: Return score + session_id
    return JSONResponse(content={
        "score": score_result,
        "session_id": session_id
    })


@app.post("/enhance")
async def enhance_candidate_resume(session_id: str = Form(...)):
    # Step 1: Fetch stored data
    if session_id not in SESSIONS:
        return JSONResponse(
            content={"error": "Invalid or expired session_id"}, 
            status_code=400
        )

    data = SESSIONS[session_id]
    resume_data = data["resume_data"]
    job_data = data["job_data"]
    file_path = data["file_path"]

    # Step 2: Convert resume file into text
    from backend.resloader import read_pdf_to_text
    resume_text = read_pdf_to_text(file_path)

    # Step 3: Enhance resume
    score, resume_enhanced = enhance_resume(job_data, resume_text, resume_data)

    # Step 4: Format resume JSON
    resume_formatted = format_resume(resume_enhanced)
    resume_dict = json.loads(resume_formatted)

    # Step 5: Generate PDF (save it with a unique name)
    output_filename = f"enhanced_{session_id}.pdf"
    # output_path = os.path.join(UPLOAD_DIR, output_filename)
    output_path=generate_resume_from_json(resume_dict)  

    # Step 6: Return PDF as response
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf"
    )
