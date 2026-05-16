import re


def load_text(path):
  text = ""
  with open(path, "r") as f:
    text = f.read()

  return text

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()