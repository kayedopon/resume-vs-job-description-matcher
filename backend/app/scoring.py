from app.skill_extraction import extract_skills
from app.similarity import tfidf_similarity, semantic_similarity

import json


def skill_match_score(resume_skills: set[str], job_skills: set[str]) -> float:
    if len(job_skills) == 0:
        return 0
    
    score = len(resume_skills.intersection(job_skills)) / len(job_skills)
    return round(score * 100, 2)

def calculate_final_score(skill_score: float, tfidf_score: float, semantic_score: float) -> float:
    final_score = 0.5 * skill_score + 0.3 * semantic_score + 0.2 * tfidf_score

    return round(final_score, 2)

def generate_suggestions(missing_skills: list[str]) -> str:
  if not missing_skills:
    return "Your resume coverts the main required skills for this job"

  missing = ", ".join(missing_skills)

  return f"Consider adding relevant experience, projects or courses related to: {missing}."



