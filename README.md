# Sembreak Project — Resume Evaluator & Enhancer

Small service that:
- Extracts structured resume data from uploaded PDFs
- Scrapes and structures job postings (Naukri.com via Selenium)
- Scores candidates against jobs (experience, education, skills via embeddings + LLM eligibility checks)
- Enhances resumes using an LLM and generates a formatted PDF

Table of contents
- Overview
- Features
- Prerequisites
- Installation
- Configuration
- Running the server
- API endpoints (examples)
- File structure (high level)
- Notes & troubleshooting

Overview
This project provides a FastAPI server that accepts a resume PDF and a job URL, scores the candidate against the job, and can produce an enhanced resume PDF. The scoring pipeline combines LLM-based eligibility checks, embedding-based skill similarity, and resume enhancement via an LLM to produce a formatted resume PDF.

Features
- Resume extraction (PDF -> structured JSON)
- Job scraping and structuring (targeted for Naukri job pages)
- Eligibility check via LLM (experience & education)
- Skill scoring using embedding model (configurable)
- Resume enhancement + PDF generation (ReportLab)
- REST API with endpoints to evaluate and enhance candidate resumes
- Session-based flow for evaluate -> enhance

Prerequisites
- OS: Linux / macOS / Windows
- Python 3.11 recommended (for torch)
- Git
- Chrome (or Chromium) + ChromeDriver if using Selenium-based job scraping
- Enough RAM / disk for ML model downloads if using transformer-based embedding models (may be large).

Installation (quick)
1. Clone the repo
   git clone https://github.com/Prathat2006/Resume-analyser-enhancer.git

   cd Resume-anlyser-enhancer

2. Create & activate virtual environment
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate

3. Install dependencies
   pip install --upgrade pip
   #for torch the check cuda install and form pytorch match the  cuda version and then install
   pip install torch
   pip install -r requirements.txt
Configuration
- .env.sample
  - GROQ_API_KEY and OPENROUTER_API_KEY placeholders for external LLM/embedding providers. Fill and save as `.env` or export environment variables as needed.

- config.ini (provided)
  - Controls LLM/embedding model names and SIM_THRESHOLD
  - Example keys:
    [llms] model =openai/gpt-oss-120b.
    [embedding_model] embedding_model = Qwen/Qwen3-Embedding-0.6B
    [SIM_THRESHOLD] skill_words_strictness = 0.8

Notes:
- If you use a local or hosted embedding model, adjust the `embedding_model` in config.ini. Large models may require GPU or significant CPU memory.
- If using transformers + torch from Hugging Face, ensure you have the correct CUDA toolkit if running on GPU.

Running the server
1. Ensure your virtualenv is active and env vars / config.ini are set.
2. Start the FastAPI server:
   uvicorn server:app --reload --host 0.0.0.0 --port 8000

3. Open http://127.0.0.1:8000/docs for interactive OpenAPI docs.

# for GUI 
run this in terminal
streamlit run ui/streamlitui.py 

# for backend
API Endpoints

1) POST /evaluate
- Purpose: Upload candidate resume (PDF) and supply a job URL. Returns candidate score and session_id for enhancement flow.
- Form fields:
  - resume: file (PDF)
  - job_url: string (job posting URL)

- Example using curl:
  curl -X POST "http://127.0.0.1:8000/evaluate" \
    -F "resume=@/path/to/resume.pdf" \
    -F "job_url=https://www.naukri.com/job-listings-..." \
    -H "Accept: application/json"

- Successful response:
  {
    "score": {
      "final_score": 85.23,
      "eligible": true
    },
    "session_id": "uuid-string"
  }

2) POST /enhance
- Purpose: Given a session_id returned by /evaluate, enhance the resume using LLM suggestions and return an enhanced PDF. X-Score header includes the enhanced candidate score JSON.
- Form fields:
  - session_id: string

- Example using curl:
  curl -X POST "http://127.0.0.1:8000/enhance" \
    -F "session_id=<session_id>" \
    -o enhanced_resume.pdf -D headers.txt

- The response is a PDF file. The server also sets header `X-Score` containing JSON with the enhanced score. Inspect headers.txt (or response headers) to view the enhanced score.

File structure (high level)
- server.py — FastAPI app with /evaluate and /enhance endpoints
- backend/
  - resume_praserer.py — parse resumes into structured data (resumes)
  - naukridotcomfetcher.py — Selenium job page scraper
  - jobdetailstructurer.py — structures job details
  - resloader.py — PDF reading helper(s)
  - embedding_scorere.py — embeddings, skill scoring and eligibility orchestration
  - json_breaker.py — helpers to extract education/experience/skills from JSON
- resume_enhancer/
  - enhance.py — main enhancement orchestration
  - formater.py — formats enhanced resume JSON
  - src/build.py — generates PDF from structured resume JSON (ReportLab)
- config.ini — model and threshold configuration
- .env.sample — env var examples for API keys

Notes & troubleshooting
- Selenium scraping: ensure ChromeDriver is installed and matches Chrome version. If scraping fails, check naukridotcomfetcher.py and Selenium logs.
- PyMuPDF import error: install with pip install pymupdf
- Transformers / Hugging Face models: model names in config.ini must be accessible. Large models may require GPU or lots of RAM.
- Embedding model warnings: if you see OOM or very slow downloads, switch to a smaller embedding model or run on a machine with more resources.
- If LLM calls fail, ensure LLM config (in config.ini / env vars) and network access / API keys are correct.
- PDF generation: generate_resume_from_json writes files in the working directory (filename derived from author). The enhance endpoint wraps this and returns a generated PDF.

Security considerations
- Do not expose large LLM/embedding models publicly without rate limiting or auth.
- Uploaded files are stored in an uploads/ directory by the server. Hardening is recommended (clean up old sessions, store files in secure storage, validate file types).

Extending & development tips
- Replace in-memory SESSIONS with Redis or database for persistence.
- Add authentication to endpoints.
- Swap embedding API with a managed vector store for large-scale scoring.
- Add retry/backoff for large model downloads or remote LLM calls.

# Important Note :
this is backend for frontend clone this repo :[<repo_url>](https://github.com/Prathat2006/Resume-analyser-enhancer-frontend.git)