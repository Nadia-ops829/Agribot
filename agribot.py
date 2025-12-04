import pandas as pd
import re
import numpy as np
import spacy
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Supprimer le warning spécifique de sklearn
warnings.filterwarnings("ignore", category=UserWarning, 
                        message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None")

# Charger le modèle spaCy françaiss_md
try:
    # Essayer d'abord le modèle medium
    nlp = spacy.load("fr_core_news_md")
    print("✓ Modèle spaCy français chargé (fr_core_news_md)")
except OSError as e:
    try:
        # Essayer le modèle small en fallback
        nlp = spacy.load("fr_core_news_md")
        print("✓ Modèle spaCy français chargé (fr_core_news_md)")
    except OSError:
        print("Aucun modèle spaCy français trouvé.")
        print("Veuillez installer un modèle avec une de ces commandes:")
        print("  python -m spacy download fr_core_news_md")
        print("  python -m spacy download fr_core_news_md")
        print("\nPour le moment, j'utilise un tokenizer simple...")
        nlp = None

def spacy_tokenizer(text):
    """
    Tokeniseur avancé utilisant spaCy pour la lemmatisation et la suppression des stop words.
    """
    if nlp:
        doc = nlp(text.lower())
        tokens = []
        for token in doc:
            # Supprimer les espaces, la ponctuation, les chiffres et les stop words
            if not token.is_space and not token.is_punct and not token.like_num and not token.is_stop:
                # Utiliser le lemme (forme de base du mot)
                tokens.append(token.lemma_)
        return tokens
    else:
        # Fallback: Tokenizer simple sans spaCy
        french_stopwords = set([
            'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou', 'mais',
            'donc', 'or', 'ni', 'car', 'à', 'au', 'aux', 'avec', 'ce', 'cet', 'cette',
            'ces', 'dans', 'en', 'pour', 'par', 'sur', 'sous', 'entre', 'qui', 'que',
            'quoi', 'dont', 'où', 'y', 'ne', 'pas', 'plus', 'moins', 'très', 'non'
        ])
        
        # Nettoyage basique
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)  # Supprimer la ponctuation
        words = text.split()
        
        # Filtrer les stop words et mots courts
        return [word for word in words if word not in french_stopwords and len(word) > 2]

class AgriBot:
    def __init__(self, csv_path="chatbot_dataset_large.csv"):
        print("\n" + "="*70)
        print("Chargement du dataset agricole et préparation du moteur IA...")
        print("="*70)
        
        try:
            # Le dataset large est maintenant la référence
            self.df = pd.read_csv(csv_path, on_bad_lines='skip', encoding='utf-8').fillna("")
        except FileNotFoundError:
            print(f"\nERREUR: Le fichier '{csv_path}' est introuvable.")
            print("Veuillez vous assurer qu'il est dans le même répertoire.")
            raise
        
        # Vérifier les colonnes nécessaires
        required_columns = ['question', 'reponse']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            print(f"\nERREUR: Colonnes manquantes dans le CSV: {', '.join(missing_columns)}")
            print(f"Colonnes disponibles: {list(self.df.columns)}")
            raise ValueError(f"Le fichier CSV doit contenir les colonnes: {', '.join(required_columns)}")
        
        print(f"✓ Dataset chargé: {len(self.df)} questions-réponses")

        # Configurer le TfidfVectorizer sans token_pattern pour éviter le warning
        self.vectorizer = TfidfVectorizer(
            tokenizer=spacy_tokenizer,
            ngram_range=(1, 3),
            lowercase=False,
            max_features=10000,  # Limiter le nombre de features pour la performance
            min_df=2,  # Ignorer les termes qui apparaissent moins de 2 fois
            max_df=0.85,  # Ignorer les termes qui apparaissent dans plus de 85% des documents
            stop_words=None,
            token_pattern=None  # Explicitement défini à None pour éviter le warning
        )
        
        print("✓ Vectoriseur TF-IDF configuré")
        
        # Entraîner le vectoriseur
        print("  Entraînement du modèle TF-IDF en cours...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['question'])
        print(f"✓ Modèle TF-IDF entraîné: {self.tfidf_matrix.shape[1]} features")
        
        self.user_data = {}
        print("✓ AgriBot prêt !")
        print("="*70)

    def extract_info(self, msg):
        """Extrait les informations personnelles du message."""
        info = {}
        
        # Extraction du nom avec des patterns améliorés
        patterns = [
            r"(je m'appelle|mon nom est|appel[ée] moi|appel[ée]-moi)\s+([A-Za-zÀ-ÿ\s-]+)",
            r"(mon pr[ée]nom est|pr[ée]nom\s*:\s*)([A-Za-zÀ-ÿ\s-]+)",
            r"^(je suis|j'suis|c'est)\s+([A-Za-zÀ-ÿ\s-]+)"
        ]
        
        for pattern in patterns:
            if m := re.search(pattern, msg, re.I):
                name = m.group(2).strip()
                if len(name.split()) <= 3:  # Éviter d'extraire des phrases complètes
                    info['name'] = name.capitalize()
                    break
        
        return info

    def find_best_answer(self, question):
        """Trouve la meilleure réponse pour une question donnée."""
        if not question.strip():
            return None, None, 0.0
        
        # Vectoriser la question
        q_vec = self.vectorizer.transform([question])
        
        # Calculer les similarités
        similarities = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        
        # Trouver les meilleures correspondances
        best_idx = similarities.argmax()
        score = similarities[best_idx]
        
        # Seuil adaptatif basé sur la longueur de la question
        threshold = max(0.15, min(0.3, len(question.split()) * 0.01))
        
        if score < threshold:
            return None, None, score
        
        row = self.df.iloc[best_idx]
        return row['reponse'], row.get('conseil', ''), score

    def respond(self, message):
        """Génère une réponse pour un message donné."""
        message = message.strip()
        
        if not message:
            return "Je suis là pour vous aider ! Posez-moi une question sur l'agriculture."
        
        # Commandes de sortie
        exit_words = ['quit', 'bye', 'au revoir', 'stop', 'exit', 'à plus', 'ciao']
        if message.lower() in exit_words:
            name = self.user_data.get('name', 'cher agriculteur')
            return f"\nAu revoir {name} ! 🌾 Bonne récolte et à bientôt pour de nouveaux conseils !"

        # Extraction des infos personnelles
        self.user_data.update(self.extract_info(message))
        name = self.user_data.get('name', 'cher agriculteur')

        # Recherche de réponse
        answer, conseil, score = self.find_best_answer(message)

        if answer:
            # Formater la réponse avec le score (seulement en mode debug)
            debug_info = f" (pertinence: {score:.1%})" if score > 0 else ""
            resp = f"Bonjour {name} !{debug_info}\n\n{answer.strip()}"
            
            if conseil and str(conseil).strip() and str(conseil).strip().lower() != 'nan':
                resp += f"\n\n **Conseil pratique** : {str(conseil).strip()}"
            
            # Ajouter une suggestion si le score n'est pas excellent
            if score < 0.4:
                resp += "\n\nℹ️  Si vous cherchez des informations plus spécifiques, n'hésitez pas à reformuler votre question."
            
            return resp
        else:
            # Réponse par défaut si aucune correspondance
            suggestions = [
                "Quels sont les prix actuels du maïs au Burkina Faso ?",
                "Comment améliorer la fertilité de mon sol ?",
                "Quelles sont les bonnes périodes pour planter le mil ?",
                "Comment protéger mes cultures contre les insectes ?",
                "Quelles sont les techniques d'irrigation économiques ?"
            ]
            
            import random
            suggestion = random.choice(suggestions)
            
            return f"""Bonjour {name} ! 👨‍🌾

Je n'ai pas trouvé d'information précise sur : "{message}"

Je peux vous aider sur des sujets comme :

🌽 **Cultures** : maïs, mil, sorgho, coton, riz
💰 **Prix des céréales** au Burkina Faso
**Météo agricole** et prévisions saisonnières
🌱 **Techniques culturales** : plantation, irrigation, fertilisation
🛡️ **Protection des cultures** contre les maladies et ravageurs
🏺 **Stockage et conservation** des récoltes

Essayez par exemple : *"{suggestion}"*

N'hésitez pas à formuler votre question autrement !"""

    def start(self):
        """Lance l'interface conversationnelle."""
        print("\n" + "="*70)
        print(" 🌾 AGRICULTURE BOT - Assistant Agricole Intelligent 🌾")
        print("="*70)
        print("\nJe suis AgriBot, votre assistant pour l'agriculture au Burkina Faso.")
        print("Posez-moi vos questions ou tapez 'au revoir' pour quitter.\n")
        
        while True:
            try:
                msg = input("\n👤 Vous : ").strip()
                if not msg:
                    continue
                
                response = self.respond(msg)
                print(f"\nAgriBot : {response}")
                
                if "Au revoir" in response:
                    print("\n" + "="*70)
                    break
                    
            except KeyboardInterrupt:
                print("\n\n Session interrompue. À bientôt !")
                break
            except Exception as e:
                print(f"\n Une erreur est survenue : {str(e)}")
                print("Veuillez reformuler votre question.")
                # Option: logger l'erreur pour debug
                # import traceback
                # traceback.print_exc()

if __name__ == "__main__":
    try:
        bot = AgriBot("dataset.csv")
        bot.start()
    except (FileNotFoundError, ValueError) as e:
        print(f"\n Erreur : {e}")
        print("\n Conseils de dépannage :")
        print("1. Vérifiez que 'dataset.csv' existe dans le dossier")
        print("2. Vérifiez que le CSV contient les colonnes 'question' et 'reponse'")
        print("3. Pour installer spaCy français :")
        print("   python -m spacy download fr_core_news_md")
    except Exception as e:
        print(f"\n💥 Une erreur inattendue est survenue : {e}")
        print("Merci de vérifier votre installation et vos données.")