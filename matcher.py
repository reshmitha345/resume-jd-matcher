from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_text_from_pdf(file_path):
    import PyPDF2
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def get_keyword_gap(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit([jd_text])
    jd_keywords = set(vectorizer.get_feature_names_out())
    resume_words = set(resume_text.lower().split())
    missing = jd_keywords - resume_words
    # Filter short words
    missing = [w for w in missing if len(w) > 3]
    return sorted(missing)[:20]