from app.skill_extraction import extract_skills
from app.similarity import skill_match_score, tfidf_similarity, semantic_similarity

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

def match_resume_to_job(resume, job, skills):
    resume_skills = set(extract_skills(resume, skills))
    job_skills = set(extract_skills(job, skills))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    skill_score = skill_match_score(resume_skills, job_skills)
    tfidf_score = tfidf_similarity(resume, job)
    semantic_score = semantic_similarity(resume, job)
    final_score = calculate_final_score(skill_score, tfidf_score, semantic_score)

    results = {
      "skill_score": skill_score,
      "tfidf_score": tfidf_score,
      "semantic_score": semantic_score,
      "final_score": final_score,
      "resume_skills": resume_skills,
      "job_skills": job_skills,
      "matched_skills": matched_skills,
      "missing_skills": missing_skills,
      "suggestion": generate_suggestions(missing_skills)
    }

    return json.dumps(results)




