from src.skill_extraction import extract_skills
from src.similarity import skill_match_score, tfidf_similarity, semantic_similarity

def generate_suggestions(missing_skills):
  if not missing_skills:
    return "Your resume coverts the main required skills for this job"

  missing = ", ".join(missing_skills)

  return f"Consider adding relevant experience, projects or courses related to: {missing}."

def score(resume, job, skills):
    resume_skills = set(extract_skills(resume, skills))
    job_skills = set(extract_skills(job, skills))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    skill_score = skill_match_score(resume_skills, job_skills)
    tfidf_score = tfidf_similarity(resume, job)
    semantic_score = semantic_similarity(resume, job)
    final_score = 0.5 * skill_score + 0.3 * semantic_score + 0.2 * tfidf_score

    results = f"""
    Skill Match Score: {skill_score}%
    TF-IDF Similarity Score: {tfidf_score}% (based on important words)
    Semantic score: {semantic_score}% (similarity by meaning)
    Final Score: {final_score}%

    Matched Skills:
    {", ".join(matched_skills)}

    Missing Skills:
    {", ".join(missing_skills)}

    Suggestion:
    {generate_suggestions(missing_skills)}
    """

    print(results)


