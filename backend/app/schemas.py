from pydantic import BaseModel
from typing import List


class MatchRequest(BaseModel):
    resume_text: str
    job_text: str
    skills: List[str]


class MatchResponse(BaseModel):
    skill_score: float
    tfidf_score: float
    semantic_score: float
    final_score: float
    resume_skills: List[str]
    job_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    suggestion: str