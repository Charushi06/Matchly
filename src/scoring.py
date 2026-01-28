from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any

class ResumeScorer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_basic_similarity(self, job_description: str, resumes: List[str]) -> List[float]:
        """
        Calculates standard cosine similarity between JD and resumes using TF-IDF.
        Returns a list of similarity scores (0-1).
        """
        if not resumes:
            return []
            
        corpus = [job_description] + resumes
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except ValueError:
            # This happens if the vocabulary is empty (e.g. all words were stop words or empty input)
            print("Warning: Empty vocabulary in TF-IDF. Returning 0 scores.")
            return [0.0] * len(resumes)
        
        jd_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
        return similarities.tolist()

    def rank_resumes(self, resumes: List[Dict[str, Any]], similarity_scores: List[float]) -> List[Dict[str, Any]]:
        """
        Attaches scores to resumes and sorts them.
        """
        ranking = []
        for i, resume in enumerate(resumes):
            entry = resume.copy()
            entry['score'] = float(similarity_scores[i])
            ranking.append(entry)
        
        # Sort by score descending
        ranking.sort(key=lambda x: x['score'], reverse=True)
        return ranking
