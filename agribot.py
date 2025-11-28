# discuter_avec_agribot_PARFAIT.py → Répond à TOUT (scrapé + manuel)


import spacy
import random
from pathlib import Path

# Import du dataset manuel (même nom que dans Django)
try:
    from chat.dataset_manuel import get_reponse_manuelle, DATASET_MANUEL
except:
    # Si tu lances depuis la racine, ça marche aussi
    import sys
    sys.path.append("chat")
    from dataset_manuel import get_reponse_manuelle, DATASET_MANUEL

print("\n" + "="*75)
print("         AGRIBOT BF – DISCUTER AVEC LE BOT AGRICOLE ULTIME")

print("="*75 + "\n")

# Chargement du modèle français avec vecteurs
try:
    nlp = spacy.load("fr_core_news_md")
    print("Modèle français avec vecteurs chargé")
except:
    print("Téléchargement du modèle français (300 Mo, 1 fois seulement)...")
    import os
    os.system("python -m spacy download fr_core_news_md")
    nlp = spacy.load("fr_core_news_md")

# Chargement du corpus scrapé
CORPUS = []
csv_path = Path("data/processed_agri/burkina_agri_corpus.csv")
if csv_path.exists():
    import csv
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) >= 3 and len(row[2]) > 100:
                texte = row[2].strip()
                if any(k in texte.lower() for k in ["burkina","coton","fcfa","ministère","campagne","zaï","tonnes","agriculture"]):
                    CORPUS.append(texte)
print(f"{len(CORPUS)} documents scrapés chargés")
print(f"{len(DATASET_MANUEL)} dataset manuels  chargées\n")

def repondre(question):
    question = question.strip()
    if not question:
        return "Pose-moi une vraie question mon frère !"

    q_lower = question.lower()

    # 1. PRIORITÉ MAX : dataset manuel (plantation, maladies, sols, etc.)
    reponse_manuelle = get_reponse_manuelle(q_lower)
    if reponse_manuelle:
        return reponse_manuelle

    # 2. Sinon : recherche dans le corpus scrapé
    doc_q = nlp(q_lower)
    meilleur_score = 0
    meilleure_reponse = random.choice(DATASET_MANUEL)  # fallback intelligent

    for texte in CORPUS:
        try:
            doc_t = nlp(texte[:1500])
            score = doc_q.similarity(doc_t)
            if score > meilleur_score:
                meilleur_score = score
                reponse_nette = texte.split("Menu")[0].split("Skip to")[0].split("Contact")[0].strip()
                if len(reponse_nette) > 80:
                    meilleure_reponse = reponse_nette[:950]
        except:
            continue

    # Si le score est trop faible → on prend une réponse manuelle quand même
    if meilleur_score < 0.58:
        return random.choice(DATASET_MANUEL)

    return meilleure_reponse

# Boucle de discussion
print("Pose-moi n'importe quelle question agricole")
print("Tape 'quitter' pour arrêter\n")

while True:
    q = input("Toi → ").strip()
    if q.lower() in ["quitter", "bye", "exit", "stop", "au revoir"]:
        print("\nAgriBot → Wend na koama ! Que Dieu bénisse ta récolte et ta famille")
        break
    print(f"AgriBot → {repondre(q)}\n")