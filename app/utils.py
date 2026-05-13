import fitz

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    doc.close()

    return text.strip()

def parse_skills(skills: str) -> list[str]:
    return [skill.strip() for skill in skills.split(", ") if skill.strip()]