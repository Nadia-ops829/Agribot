import pickle
import os
import numpy as np
from django.conf import settings
import warnings
warnings.filterwarnings("ignore")

class ChatBotService:
    """
    Service singleton pour le chatbot agricole.
    Charge le modèle TF-IDF pré-entraîné une seule fois en mémoire.
    """
    _instance = None
    _model_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._model_loaded:
            self.vectorizer = None
            self.tfidf_matrix = None
            self.df = None
            self._load_model()
            self._model_loaded = True
    
 
    def _load_model(self):
        """Charge le modèle pré-entraîné depuis le cache"""
        try:
            model_dir = os.path.join(settings.BASE_DIR, 'model_cache')
            
            print(f"📁 Recherche du modèle dans: {model_dir}")
            
            # Vérifier si le répertoire existe
            if not os.path.exists(model_dir):
                print(f"Répertoire modèle introuvable: {model_dir}")
                print("   Exécutez: python manage.py train_chatbot")
                return
            
            # Liste des fichiers disponibles
            files = os.listdir(model_dir)
            print(f"📄 Fichiers trouvés: {files}")
            
            # Charger le vectorizer
            vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
            if os.path.exists(vectorizer_path):
                print("   Chargement du vectorizer...")
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print(f"   ✓ Vectorizer chargé: {type(self.vectorizer)}")
            else:
                print(f"Fichier vectorizer introuvable: {vectorizer_path}")
                return
            
            # Charger la matrice TF-IDF
            import scipy.sparse
            matrix_path = os.path.join(model_dir, 'tfidf_matrix.pkl')
            if os.path.exists(matrix_path):
                print("   Chargement de la matrice TF-IDF...")
                with open(matrix_path, 'rb') as f:
                    pickle.load(f)  # Lire la fonction save_npz
                    self.tfidf_matrix = scipy.sparse.load_npz(f)
                print(f"   ✓ Matrice TF-IDF chargée: {self.tfidf_matrix.shape}")
            else:
                print(f"Fichier matrice introuvable: {matrix_path}")
                return
            
            # Charger le dataset
            dataset_path = os.path.join(model_dir, 'dataset.pkl')
            if os.path.exists(dataset_path):
                print("   Chargement du dataset...")
                with open(dataset_path, 'rb') as f:
                    self.df = pickle.load(f)
                print(f"   ✓ Dataset chargé: {len(self.df)} questions")
                print(f"   ✓ Colonnes: {list(self.df.columns)}")
                
                # Afficher quelques exemples
                print("   Exemples de questions:")
                for i in range(min(3, len(self.df))):
                    print(f"      {i+1}. {self.df.iloc[i]['question'][:50]}...")
            else:
                print(f"Fichier dataset introuvable: {dataset_path}")
                return
            
            print(f"✅ Modèle chatbot chargé avec succès!")
            
        except Exception as e:
            print(f"Erreur chargement modèle: {e}")
            import traceback
            traceback.print_exc()
            self.vectorizer = None
            self.tfidf_matrix = None
            self.df = None
    
    def get_response(self, question, user_name="l'agriculteur"):
        """Retourne une réponse basée sur la similarité TF-IDF"""
        if not self.vectorizer or not self.tfidf_matrix or not self.df:
            print("Modèle non chargé, retour réponse par défaut")
            return {
                'answer': f"Bonjour {user_name}, le service chatbot est en cours de préparation. Revenez dans quelques instants.",
                'score': 0,
                'status': 'error'
            }
        
        try:
            print(f"\nRecherche pour: '{question}'")
            
            # Vectorisation de la question
            q_vec = self.vectorizer.transform([question])
            print(f"   ✓ Question vectorisée")
            
            # Calcul de similarité cosinus
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
            best_idx = similarities.argmax()
            score = similarities[best_idx]
            
            print(f"   ✓ Score max: {score:.3f} (index: {best_idx})")
            
            # Seuil de confiance (baissé pour plus de tolérance)
            threshold = 0.05  # Baissé de 0.15 à 0.05
            
            if score < threshold:
                print(f"   Score trop bas (< {threshold}), retour réponse par défaut")
                return {
                    'answer': f"Bonjour {user_name}",
                    'score': float(score),
                    'status': 'low_confidence'
                }
            
            # Récupérer la meilleure réponse
            row = self.df.iloc[best_idx]
            print(f"   ✓ Question trouvée: '{row['question'][:50]}...'")
            print(f"   ✓ Réponse: '{row['reponse'][:50]}...'")
            
            return {
                'answer': row['reponse'],
                'conseil': row.get('conseil', ''),
                'score': float(score),
                'status': 'success'
            }
            
        except Exception as e:
            print(f"Erreur recherche réponse: {e}")
            import traceback
            traceback.print_exc()
            return {
                'answer': f"Bonjour {user_name}, une erreur est survenue. Reformulez votre question.",
                'score': 0,
                'status': 'error'
            }
    
    def is_ready(self):
        """Vérifie si le service est prêt"""
        return self.vectorizer is not None and self.tfidf_matrix is not None

# Instance globale pour Django
chatbot_service = ChatBotService()