# chat/engine.py → VERSION QUI MARCHE À COUP SÛR (décembre 2025)

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .dataset_manuel import DATASET_MANUEL

# On vectorise DIRECTEMENT les réponses du dataset manuel
vectorizer = TfidfVectorizer(
    ngram_range=(1, 4),
    lowercase=True,
    strip_accents='unicode',
    stop_words=None
)

# On crée la matrice TF-IDF une seule fois au démarrage
tfidf_matrix = vectorizer.fit_transform(DATASET_MANUEL)

def get_best_response(question):
    # Nettoyage ultra-simple
    q = question.lower()
    q = re.sub(r'[^\w\s]', ' ', q)

    # Vectorisation de la question
    q_vec = vectorizer.transform([q])

    # Similarité cosine
    similarities = cosine_similarity(q_vec, tfidf_matrix).flatten()
    best_idx = np.argmax(similarities)
    score = similarities[best_idx]

    # Seuil très bas mais intelligent (0.08 = magique avec ton dataset)
    if score > 0.08:
        return DATASET_MANUEL[best_idx]

    return None