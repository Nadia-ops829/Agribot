# chat/views.py → VERSION FINALE QUI MARCHE À COUP SÛR

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

# Météo
from .tools.weather import get_meteo, get_previsions, alerte_risque

# Le moteur magique (plus de classe, juste une fonction)
from .engine import get_best_response


def chat_view(request):
    return render(request, 'index.html')


@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST requis"}, status=400)

    message = request.POST.get("message", "").strip()
    if not message:
        return JsonResponse({"response": "Pose-moi une question mon frère !"})

    msg_lower = message.lower()

    message_lower = message.lower()

    # === 1. Météo en priorité ===
    if any(m in message_lower for m in ["météo","temps","pluie","demain","prévision","alerte","sécheresse","inondation","chaud","froid"]):
        ville = "Ouagadougou"
        villes = {"bobo":"Bobo-Dioulasso", "ouaga":"Ouagadougou", "kaya":"Kaya", "fada":"Fada N'gourma", "banfora":"Banfora"}
        for short, full in villes.items():
            if short in message_lower:
                ville = full
                break
        meteo = get_meteo(ville)
        prev = get_previsions(ville)
        alerte = alerte_risque(ville)
        return JsonResponse({"response": f"{meteo}\n\n{prev}\n\n{alerte}".strip()})

    # === 2. Réponse depuis le dataset manuel (le cœur du bot) ===
    reponse = get_best_response(message)
    if reponse:
        return JsonResponse({"response": reponse})

    # === 3. Si vraiment rien ne matche ===
    defaults = [
        "Je n’ai pas bien compris, mais je peux t’aider sur : prix du coton, zaï, VDP, crédit, maladies, variétés, Président… Pose-moi ta question autrement mon frère !",
        "Wend na kodô ! Tu veux savoir quoi exactement ? Coton ? Sol ? Maladies ? Crédit ? Je suis là.",
        "Dis-moi ton problème : sécheresse ? chenille ? striga ? prix ? sol dégradé ? Je connais tout ça !"
    ]
    return JsonResponse({"response": random.choice(defaults)})