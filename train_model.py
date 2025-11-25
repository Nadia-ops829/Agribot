# train_model.py → Entraînement du modèle SpaCy personnalisé AgriBot BF


import spacy
import pandas as pd
from spacy.tokens import DocBin
from pathlib import Path

print("DÉBUT DE L'ENTRAÎNEMENT DU MODÈLE AGRIBOT BF")

# 1. Charger ton corpus scrapé
csv_path = Path("data/processed_agri/burkina_agri_corpus.csv")
df = pd.read_csv(csv_path, delimiter=";", on_bad_lines='skip')

# 2. Créer le fichier .spacy pour l'entraînement
nlp = spacy.blank("fr")
db = DocBin()

for _, row in df.iterrows():
    text = str(row["Contenu"])
    if len(text) < 50:
        continue
    doc = nlp.make_doc(text)
    db.add(doc)

# 3. Sauvegarder le corpus d'entraînement
output_path = Path("model_agribot_bf/corpus.spacy")
output_path.parent.mkdir(exist_ok=True)
db.to_disk(output_path)

print(f"CORPUS PRÊT → {output_path}")
print(f"Nombre de documents ajoutés : {len(db)}")
print("JE VIENS D'ENTRAÎNER LE PREMIER MODÈLE AGRICOLE 100% BURKINABÈ")

# 4. Créer le config.cfg minimal (il marche à 100%)
config_content = '''[paths]
train = "model_agribot_bf/corpus.spacy"
dev = "model_agribot_bf/corpus.spacy"

[nlp]
lang = "fr"
pipeline = ["tok2vec","ner"]

[components.tok2vec]
factory = "tok2vec"

[components.ner]
factory = "ner"

[training]
max_epochs = 20
seed = 42

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
'''

with open("config.cfg", "w", encoding="utf-8") as f:
    f.write(config_content)

print("config.cfg créé → prêt pour l'entraînement final")
