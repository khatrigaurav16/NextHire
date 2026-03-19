import sys
import os

_additional_path = r"C:\Users\gaura\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages"
if _additional_path not in sys.path:
    sys.path.insert(0, _additional_path)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI(title="NextHire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")


class KeywordsRequest(BaseModel):
    summary: str


class KeywordsResponse(BaseModel):
    keywords: str


def extract_text_from_pdf(uploaded_file: UploadFile) -> str:
    doc = fitz.open(stream=uploaded_file.file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_gemini(prompt: str, max_tokens: int = 500) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key not configured"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


@app.post("/api/analyze")
async def analyze_resume(file: UploadFile = File(...), location: str = "India"):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        resume_text = extract_text_from_pdf(file)

        summary = ask_gemini(
            f"Summarize the following resume highlighting the key skills, experiences, and education in a clear, concise format:\n\n{resume_text}",
            max_tokens=500,
        )

        skill_gaps = ask_gemini(
            f"Based on the following resume, identify skill gaps and areas for improvement. Format as bullet points:\n\n{resume_text}",
            max_tokens=400,
        )

        roadmap = ask_gemini(
            f"Based on the resume and skill gaps, create a learning roadmap with specific steps:\n\nResume:\n{resume_text}\n\nSkill Gaps:\n{skill_gaps}",
            max_tokens=400,
        )

        keywords = ask_gemini(
            f"Based on this resume summary, suggest 3-5 job search keywords. Return only comma-separated keywords:\n\n{summary}",
            max_tokens=50,
        )

        return {
            "success": True,
            "data": {
                "summary": summary,
                "skillGaps": skill_gaps,
                "roadmap": roadmap,
                "keywords": keywords.replace("\n", "").strip(),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/jobs")
async def get_jobs(keywords: str, location: str = "India"):
    jobs = []

    try:
        url = "https://api.joinrise.io/api/v1/jobs/public"
        response = requests.get(url, params={"page": 1, "limit": 100})

        if response.status_code == 200:
            data = response.json()
            jobs_data = data.get("result", {}).get("jobs", [])

            search_terms = keywords.lower().split()

            for job in jobs_data:
                title = job.get("title", "").lower()
                desc = (
                    job.get("descriptionBreakdown", {})
                    .get("oneSentenceJobSummary", "")
                    .lower()
                )
                combined = title + " " + desc

                if any(term in combined for term in search_terms):
                    jobs.append(
                        {
                            "id": str(job.get("id", "")),
                            "title": job.get("title", "N/A"),
                            "companyName": job.get("owner", {}).get(
                                "companyName", "N/A"
                            ),
                            "location": job.get("locationAddress", "N/A"),
                            "type": job.get("type", "N/A"),
                            "seniority": job.get("seniority", "N/A"),
                            "skills": job.get("skills_suggest", [])[:5],
                            "link": job.get("url", "#"),
                        }
                    )

                if len(jobs) >= 15:
                    break
    except Exception as e:
        print(f"Error fetching jobs: {e}")

    return {"success": True, "data": jobs}


@app.post("/api/keywords")
async def generate_keywords(request: KeywordsRequest):
    keywords = ask_gemini(
        f"Based on this resume summary, suggest 3-5 job search keywords. Return only comma-separated keywords:\n\n{request.summary}",
        max_tokens=50,
    )

    return {"success": True, "data": {"keywords": keywords.replace("\n", "").strip()}}


@app.get("/")
async def root():
    return {"message": "NextHire API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
