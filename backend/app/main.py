from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.llm_service import analyze_resume
from app.services.job_parser import extract_job_page
from app.prompts import build_resume_analysis_prompt
import tempfile


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "message": "ResumePilot backend is running!"
    }


@app.post("/ask")
def ask(request: PromptRequest):
    answer = analyze_resume(request.prompt)

    return {
        "answer": answer
    }


@app.post("/analyze-url")
def analyze_url(
    file: UploadFile = File(...),
    url: str = Form(...)
):
    # Save the uploaded resume temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    # Extract resume text
    from app.services.resume_parser import extract_resume_text

    resume_text = extract_resume_text(temp_file_path)

    # Extract and clean the job description from the URL
    text = extract_job_page(url)

    if not text.strip():
        return {
            "filename": file.filename,
            "url": url,
            "job_description_found": False,
            "message": "No job description was found. Please paste the job description instead."
        }

    from app.services.llm_service import extract_job_description
    job_description = extract_job_description(text)
    
    if job_description == "No job posting content found.":
        return {
            "filename": file.filename,
            "url": url,
            "job_description_found": False,
            "message": "No job description was found. Please paste the job description instead."
        }

    # Build the AI prompt
    prompt = build_resume_analysis_prompt(
        resume_text,
        job_description
    )

    # Analyze the resume against the job description
    answer = analyze_resume(prompt)

    return {
        "filename": file.filename,
        "url": url,
        "job_description": job_description,
        "analysis": answer.model_dump()
    }


@app.post("/analyze-job-desc")
def analyze_job_desc(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Save the uploaded resume temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    # Extract resume text
    from app.services.resume_parser import extract_resume_text

    resume_text = extract_resume_text(temp_file_path)

    # Build the AI prompt
    prompt = build_resume_analysis_prompt(
        resume_text,
        job_description
    )

    # Analyze the resume against the job description
    answer = analyze_resume(prompt)

    return {
        "filename": file.filename,
        "analysis": answer.model_dump()
    }


@app.post("/test-job-url")
def test_job_url(url: str):
    text = extract_job_page(url)

    return {
        "url": url,
        "extracted_text": text
    }


@app.post("/test-job-url-clean")
def test_job_url_clean(url: str):
    text = extract_job_page(url)

    from app.services.llm_service import extract_job_description

    cleaned_text = extract_job_description(text)

    return {
        "url": url,
        "cleaned_job_description": cleaned_text
    }


@app.post("/test-job-url-raw")
def test_job_url_raw(url: str):
    text = extract_job_page(url)

    return {
        "url": url,
        "extracted_text": text
    }


@app.post("/test-job-url-frames")
def test_job_url_frames(url: str):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        frames = []

        for frame in page.frames:
            try:
                text = frame.locator("body").inner_text()

                frames.append({
                    "url": frame.url,
                    "name": frame.name,
                    "text": text
                })

            except Exception as e:
                frames.append({
                    "url": frame.url,
                    "name": frame.name,
                    "error": str(e)
                })

        browser.close()

    return {
        "url": url,
        "frames": frames
    }


@app.post("/test-job-url-playwright")
def test_job_url_playwright(url: str):
    from app.services.job_parser import extract_with_playwright

    text = extract_with_playwright(url)

    return {
        "url": url,
        "extracted_text": text
    }