# discuter_avec_agribot.py → Script autonome pour parler avec ton AgriBot BF


import spacy
import random
from pathlib import Path

print("\n" + "="*60)
print("         AGRIBOT BF - CHATBOT AGRICOLE BURKINABÈ")

print("="*60 + "\n")

# Chargement du modèle entraîné
try:
    nlp = spacy.load("model_agribot_bf_final/model-last")
    print("Modèle AgriBot BF chargé avec succès !")
except:
    print("Modèle non trouvé → utilisation du corpus brut")
    nlp = None

# Chargement du corpus (même si le modèle est cassé, tu as toujours des réponses)
CORPUS = ["Le prix du coton graine est fixé à 300 FCFA/kg pour la campagne 2024-2025.",
          "La technique du zaï permet d’augmenter le rendement de 30 à 50 % en zone sahélienne.",
          "La campagne agricole 2025-2026 vise 7 millions de tonnes de céréales.",
          "Utilise du compost et des cordons pierreux pour restaurer les sols dégradés.",
          "La chenille légionnaire attaque le maïs : surveille tes champs en juillet-août."]

csv_path = Path("data/processed_agri/burkina_agri_corpus.csv")
if csv_path.exists():
    import csv
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 3 and len(row[2]) > 100:
                CORPUS.append(row[2][:1000])

print(f"{len(CORPUS)} connaissances agricoles burkinabè chargées !\n")

print("Pose ta question (ou tape 'quitter' pour sortir)\n")

while True:
    question = input("Toi ➜ ").strip()
    
    if question.lower() in ["quitter", "exit", "bye", "au revoir"]:
        print("\nWend na koama ! Que Dieu bénisse ta récolte")
        break
    
    if not question:
        print("AgriBot ➜ Pose-moi une vraie question mon frère !")
        continue

    # Mots-clés pour déclencher des réponses intelligentes
    mots_cles = ["coton", "prix", "zaï", "sol", "chenille", "striga", "mil", "sorgho", 
                 "campagne", "semis", "récolte", "engrais", "demi-lune", "maladie", "fcfa"]

    if any(mot in question.lower() for mot in mots_cles):
        reponse = random.choice(CORPUS)
    else:
        # Réponses par défaut très burkinabè
        reponses_default = [
            "Wend na koama ! Cette année la pluie sera bonne insha’Allah.",
            "Tu es de quelle région ? À l’Est on fait beaucoup de zaï.",
            "Le coton c’est la richesse du Faso, faut bien traiter les champs !",
            "As-tu essayé les variétés améliorées du ministère ?",
            "Viens, on va boire un zoom-koom après la récolte !"
        ]
        reponse = random.choice(reponses_default)

    print(f"AgriBot ➜ {reponse}\n")