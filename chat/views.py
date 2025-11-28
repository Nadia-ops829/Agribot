# chat/views.py → VERSION FINALE 20/20 — Nadia 2025
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import spacy
import random
from pathlib import Path
import csv

# Import de l'API météo + données manuelles
from .tools.weather import get_meteo, get_previsions, alerte_risque
from .dataset_manuel import get_reponse_manuelle, DATASET_MANUEL

# Modèle français avec vecteurs (réponses intelligentes)
nlp = spacy.load("fr_core_news_md")

# Chargement du corpus scrapé
CORPUS = []
csv_path = Path("data/processed_agri/burkina_agri_corpus.csv")
if csv_path.exists():
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) >= 3 and len(row[2]) > 100:
                texte = row[2].strip()
                if any(mot in texte.lower() for mot in ["burkina","coton","fcfa","ministère","campagne","zaï","tonnes"]):
                    CORPUS.append(texte)

# Vue principale
def chat_view(request):
    return render(request, 'index.html')

# Chatbot principal (tout passe par ici)
@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST requis"}, status=400)

    message = request.POST.get("message", "").strip()
    if not message:
        return JsonResponse({"response": "Pose-moi une vraie question mon frère !"})

    message_lower = message.lower()

    # 1. Données manuelles (plantation, maladies, sols, récolte)
    reponse = get_reponse_manuelle(message_lower)
    if reponse:
        return JsonResponse({"response": reponse})

    # 2. Météo en temps réel + alertes
    if any(mot in message_lower for mot in ["météo","temps","pluie","demain","prévision","alerte","sécheresse","inondation"]):
        ville = "Ouagadougou"
        villes = {"bobo":"Bobo-Dioulasso", "ouaga":"Ouagadougou", "kaya":"Kaya", "fada":"Fada N'gourma", "banfora":"Banfora"}
        for short, full in villes.items():
            if short in message_lower:
                ville = full
                break
        
        meteo = get_meteo(ville)
        prev = get_previsions(ville)
        alerte = alerte_risque(ville)
        response = f"{meteo}\n{prev}\n{alerte}"
        return JsonResponse({"response": response})

    # 3. Recherche dans le corpus scrapé
    doc_q = nlp(message_lower)
    meilleur_score = 0
    reponse_corpus = random.choice(DATASET_MANUEL)
    for texte in CORPUS:
        try:
            score = doc_q.similarity(nlp(texte[:1500]))
            if score > meilleur_score:
                meilleur_score = score
                reponse_corpus = texte[:900].strip() + "…"
        except:
            continue
    
    if meilleur_score > 0.6:
        return JsonResponse({"response": reponse_corpus})

    # 4. Réponse par défaut très burkinabè
    defaults = [
        "Le prix du coton 2024-2025 est de 325 FCFA/kg (1er choix).",
        "La campagne vise 7 millions de tonnes de céréales cette année.",
        "Utilise le zaï + compost + demi-lunes pour restaurer ton sol.",
        "Wend na koama ! Que Dieu bénisse ta récolte ma sœur !"
    ]
    return JsonResponse({"response": random.choice(defaults)})