from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import MatchRequest, MatchResponse
from app.skill_extraction import extract_skills
from app.similarity import tfidf_similarity, semantic_similarity
from app.scoring import (
    skill_match_score,
    calculate_final_score,
    generate_suggestions
)
from app.utils import extract_text_from_pdf_bytes, parse_skills


app = FastAPI(
    title="Resume vs Job Description Matcher API",
    description="NLP API for comparing resumes with job descriptions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://frontend-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match-pdf")
async def match_pdf_file(
    file: UploadFile = File(...),
    job_text:str = Form(...),
    skills: str = Form(...)):

    pdf_bytes = await file.read()
    text = extract_text_from_pdf_bytes(pdf_bytes)
    skills = parse_skills(skills)

    request = MatchRequest(
        resume_text=text,
        job_text=job_text,
        skills=skills
    )
    return match_resume_to_job(request)

@app.post("/match", response_model=MatchResponse)
def match_resume_to_job(request: MatchRequest):
    resume_skills = set(extract_skills(request.resume_text, request.skills))
    job_skills = set(extract_skills(request.job_text, request.skills))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    skill_score = skill_match_score(resume_skills, job_skills)
    tfidf_score = tfidf_similarity(request.resume_text, request.job_text)
    semantic_score = semantic_similarity(request.resume_text, request.job_text)
    final_score = calculate_final_score(skill_score, tfidf_score, semantic_score)
    suggestion = generate_suggestions(missing_skills)

    return MatchResponse(
        skill_score=skill_score,
        tfidf_score=tfidf_score,
        semantic_score=semantic_score,
        final_score=final_score,
        resume_skills=sorted(resume_skills),
        job_skills=sorted(job_skills),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestion=suggestion
    )
