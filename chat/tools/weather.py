# chat/tools/weather.py → API OpenWeatherMap complète pour AgriBot BF
# Nadia 2025 — Prévisions + alertes personnalisées

import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_meteo(ville="Ouagadougou"):
    """Météo actuelle pour une ville burkinabè."""
    if not API_KEY:
        return "Clé API manquante. Inscris-toi sur openweathermap.org"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville},BF&appid={API_KEY}&units=metric&lang=fr"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            humid = data["main"]["humidity"]
            vent = data["wind"]["speed"]
            return f"À {ville} : {temp}°C, {desc}. Humidité : {humid}%, vent : {vent} km/h."
        else:
            return f"Erreur pour {ville}. Essaie 'Ouagadougou' ou 'Bobo-Dioulasso'."
    except Exception as e:
        return f"Problème de connexion : {str(e)}"

def get_previsions(ville="Ouagadougou"):
    """Prévision pour demain."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville},BF&appid={API_KEY}&units=metric&lang=fr"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()["list"][0]  # Demain à midi
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            return f"Demain à {ville} : {temp}°C, {desc}."
        else:
            return "Prévisions indisponibles pour demain."
    except:
        return "Erreur de prévision. Vérifie ton internet."

def alerte_risque(ville="Ouagadougou"):
    """Alerte simple basée sur la prévision."""
    prev = get_previsions(ville)
    if "pluie" in prev.lower() or "orages" in prev.lower():
        return f"🚨 ALERTE à {ville} : Risque d'inondation. Prépare le drainage !"
    if "chaud" in prev.lower() or "sécheresse" in prev.lower():
        return f"⚠️ ALERTE à {ville} : Risque de sécheresse. Irrigue si possible !"
    return f"✅ Pas d'alerte majeure à {ville} demain."

def get_temperature_ouagadougou():
    """Fonction originale (bonus)."""
    return get_meteo("Ouagadougou")