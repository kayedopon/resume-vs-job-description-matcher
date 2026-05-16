from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

from backend.app.preprocessing import clean_text


def tfidf_similarity(resume_text, job_text):
  texts = [clean_text(resume_text), clean_text(job_text)]

  vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
  tfidf_matrix = vectorizer.fit_transform(texts)
  score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

  return round(score * 100, 2)

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(resume_text, job_text):
    embeddings = model.encode([resume_text, job_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(score * 100, 2)