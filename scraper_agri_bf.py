# scraper_agri_bf.py 


import time
import csv
import logging
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

#  SOURCES OFFICIELLES + MALADIES + SOLS (testées le 25/11/2025)
URLS = [
    # Sources générales sur l'agriculture au Burkina Faso
    "https://lefaso.net/spip.php?rubrique23",
    "https://www.burkina24.com/category/economie/agriculture/",
    "https://www.agriculture.bf/",
    "https://www.presidencedufaso.bf/campagne-agricole-2024-2025-plus-de-6-millions-de-tonnes-de-cereales-produites/",
    "https://www.sidwaya.info/campagne-agropastorale-2025-2026-7-millions-de-tonnes-de-cereales-attendues/",
    
    # MALADIES & RAVAGEURS (plein de détails)
    "https://www.inera.bf/recherche/sante-des-plantes/",                                           # INERA santé des plantes
    "https://www.cirad.fr/nos-recherches/filieres-tropicales/coton/protection-du-coton",          # Chenilles, fusariose, etc.
    "https://www.icrisat.org/fr/what-we-do/crop-improvement/plant-health/",                       # Striga, mildiou, aflatoxines
    "https://www.iita.org/fr/crops/cowpea/pests-and-diseases/",                                   # Maladies du niébé
    "https://www.fao.org/burkina-faso/programmes-et-projets/protection-des-plantes/fr/",          # FAO Burkina – ravageurs
    
    # SOLS, TYPES DE SOL, ANALYSE DE SOL, FERTILITÉ
    "https://www.inera.bf/recherche/sols-eau-environnement/",                                     # INERA sols & fertilité
    "https://www.agriculture.bf/index.php/fr/component/content/article/103",                     # Types de sols au Burkina (Ministère)
    "https://www.fao.org/3/ca7268fr/ca7268fr.pdf",                                                # FAO – Gestion durable des sols au Sahel (PDF riche)
    "https://www.giz.de/en/worldwide/13852.html",                                                 # GIZ Burkina – conservation des sols (zaï, demi-lune)
    "https://www.agrhymet.ne/spip.php?rubrique25", 
                                                   
     "https://www.fao.org/3/cc1229fr/cc1229fr.pdf",                                                 # Chenille, striga, etc.
    "https://www.helvetas.org/wp-content/uploads/2023/06/Guide-pratique-Zai-Burkina.pdf",
    "https://www.agrhymet.ne/IMG/pdf/Note_technique_sols_Sahel.pdf",                                               # AGRHYMET – érosion et fertilité des sols
]

def scrape(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=30, verify=False)
        if r.status_code != 200:
            logger.warning(f"Code {r.status_code} → {url}")
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        title = soup.find("title")
        title = title.get_text(strip=True) if title else "Agriculture Burkina Faso"
        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        if len(text) < 300:
            return None
        logger.info(f"SUCCÈS → {title[:70]}...")
        return {"url": url, "titre": title, "contenu": text[:20000], "type": "site_web"}
    except Exception as e:
        logger.error(f"ÉCHEC → {url} | {str(e)[:80]}")
        return None

def main():
    logger.info("SCRAPER ULTIME AGRIBOT BF ")
    corpus = []
    for url in URLS:
        doc = scrape(url)
        if doc:
            corpus.append(doc)
        time.sleep(3)  

    Path("data/processed_agri").mkdir(parents=True, exist_ok=True)
    csv_path = "data/processed_agri/burkina_agri_corpus.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["URL", "Titre", "Contenu", "Type"])
        for doc in corpus:
            writer.writerow([doc["url"], doc["titre"], doc["contenu"], doc["type"]])

    print("\n" + "="*80)
    print("CORPUS PRÊT (MALADIES + SOLS + FERTILITÉ)")
    
    print(f"→ Fichier CSV : {csv_path}")

    
    print("="*80)

if __name__ == "__main__":
    main()