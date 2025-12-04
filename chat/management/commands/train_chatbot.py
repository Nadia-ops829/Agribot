import pandas as pd
import pickle
import os
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
import hashlib
import spacy
import warnings
warnings.filterwarnings("ignore")

class Command(BaseCommand):
    help = 'Entraîne le modèle du chatbot agricole avec TF-IDF et spaCy'
    
    def handle(self, *args, **options):
        self.stdout.write("🌾 Début de l'entraînement du chatbot agricole...")
        
        # Chemins
        dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'dataset.csv')
        model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                 'model_cache')
        
        os.makedirs(model_dir, exist_ok=True)
        
        # 1. Charger le dataset
        try:
            df = pd.read_csv(dataset_path, on_bad_lines='skip', encoding='utf-8').fillna("")
            self.stdout.write(f"   ✓ Dataset chargé: {len(df)} questions")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur chargement CSV: {e}"))
            return
        
        # 2. Vérifier les colonnes nécessaires
        if 'question' not in df.columns or 'reponse' not in df.columns:
            self.stdout.write(self.style.ERROR("Le CSV doit contenir 'question' et 'reponse'"))
            return
        
        # 3. Tokenizer avec spaCy
        try:
            nlp = spacy.load("fr_core_news_md")
            
            def spacy_tokenizer(text):
                if not isinstance(text, str):
                    return []
                doc = nlp(text.lower())
                return [token.lemma_ for token in doc 
                        if not token.is_space and not token.is_punct 
                        and not token.like_num and not token.is_stop]
            
            self.stdout.write("   ✓ Tokenizer spaCy chargé")
            use_spacy = True
            
        except Exception as e:
            self.stdout.write(f"spaCy non disponible: {e}")
            
            # Tokenizer simple fallback
            french_stopwords = set([
                'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou', 'mais',
                'donc', 'or', 'ni', 'car', 'à', 'au', 'aux', 'avec', 'ce', 'cet', 'cette',
                'ces', 'dans', 'en', 'pour', 'par', 'sur', 'sous', 'entre', 'qui', 'que',
                'quoi', 'dont', 'où', 'y', 'ne', 'pas', 'plus', 'moins', 'très', 'non'
            ])
            
            def spacy_tokenizer(text):
                if not isinstance(text, str):
                    return []
                text = text.lower()
                words = text.split()
                return [w for w in words if w not in french_stopwords and len(w) > 2]
            
            use_spacy = False
        
        # 4. Entraîner TF-IDF
        try:
            vectorizer = TfidfVectorizer(
                tokenizer=spacy_tokenizer,
                ngram_range=(1, 3),
                max_features=10000,
                min_df=2,
                max_df=0.85,
                lowercase=False
            )
            
            tfidf_matrix = vectorizer.fit_transform(df['question'])
            self.stdout.write(f"   ✓ TF-IDF entraîné: {tfidf_matrix.shape[1]} features")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur entraînement TF-IDF: {e}"))
            return
        
        # 5. Sauvegarder le modèle
        try:
            # Vectorizer
            with open(os.path.join(model_dir, 'vectorizer.pkl'), 'wb') as f:
                pickle.dump(vectorizer, f)
            
            # Matrice
            with open(os.path.join(model_dir, 'tfidf_matrix.pkl'), 'wb') as f:
                pickle.dump(scipy.sparse.save_npz, f)
                scipy.sparse.save_npz(f, tfidf_matrix)
            
            # Dataset
            with open(os.path.join(model_dir, 'dataset.pkl'), 'wb') as f:
                pickle.dump(df, f)
            
            # Hash pour détecter modifications
            with open(dataset_path, 'rb') as f:
                dataset_hash = hashlib.md5(f.read()).hexdigest()
            
            with open(os.path.join(model_dir, 'dataset_hash.txt'), 'w') as f:
                f.write(dataset_hash)
            
            self.stdout.write(self.style.SUCCESS(
                f"Modèle sauvegardé dans '{model_dir}'!\n"
                f"   • {len(df)} questions\n"
                f"   • {tfidf_matrix.shape[1]} features\n"
                f"   • spaCy: {'oui' if use_spacy else 'non'}"
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur sauvegarde modèle: {e}"))