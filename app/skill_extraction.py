from app.preprocessing import clean_text

import re


def extract_skills(text, skill_list):
  text = clean_text(text)
  found_skills = []

  for skill in skill_list:
    pattern = r"\b" + re.escape(skill.lower()) + r"\b"
    if re.search(pattern, text):
      found_skills.append(skill)

  return sorted(set(found_skills))
