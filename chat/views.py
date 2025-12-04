from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json

# Météo
from .tools.weather import get_meteo, get_previsions, alerte_risque

# Nouveau moteur avec TF-IDF
from .services.chatbot_service import chatbot_service

def chat_view(request):
    return render(request, 'index.html')

@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST requis"}, status=400)
    
    # Récupérer le message
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        message = data.get("message", "").strip()
    else:
        message = request.POST.get("message", "").strip()
    
    if not message:
        return JsonResponse({"response": "Pose-moi une question mon frère !"})
    
    message_lower = message.lower()
    
    print(f"\nRequête reçue: '{message}'")
    
    # === 1. Météo en priorité ===
    if any(m in message_lower for m in ["météo","temps","pluie","demain","prévision","alerte","sécheresse","inondation","chaud","froid"]):
        print("   Détection météo")
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
    
    # === 2. Utiliser le nouveau moteur TF-IDF ===
    print("   Utilisation du chatbot_service...")
    
    if chatbot_service.is_ready():
        print("  Service prêt")
        
        # Extraire le nom de l'utilisateur si présent
        user_name = "l'agriculteur"
        name_patterns = [
            r"(je m'appelle|mon nom est|appel[ée] moi)\s+([A-Za-zÀ-ÿ\s-]+)",
            r"^(je suis|c'est)\s+([A-Za-zÀ-ÿ\s-]+)"
        ]
        
        import re
        for pattern in name_patterns:
            match = re.search(pattern, message, re.I)
            if match:
                name = match.group(2).strip()
                if len(name.split()) <= 3:
                    user_name = name.capitalize()
                    break
        
        # Obtenir la réponse du service chatbot
        response_data = chatbot_service.get_response(message, user_name)
        
        print(f"   Résultat: {response_data['status']} (score: {response_data['score']:.3f})")
        
        if response_data['status'] == 'success':
            answer = response_data['answer']
            if response_data.get('conseil'):
                answer += f"\n\n **Conseil pratique** : {response_data['conseil']}"
            
            return JsonResponse({"response": answer})
        
        elif response_data['status'] == 'low_confidence':
            # Si confiance faible, tenter de trouver des réponses dans le dataset manuellement
            print("   Tentative de recherche manuelle...")
            
            # Recherche par mots-clés simples
            keywords = {
                'striga': ['striga', 'parasite', 'mauvaises herbes', 'herbe'],
                'coton': ['coton', 'prix', 'cours', 'marché'],
                'fertilité': ['fertilité', 'sol', 'engrais', 'fumier', 'compost'],
                'maïs': ['maïs', 'mais', 'zea mays'],
                'riz': ['riz', 'paddy'],
                'mil': ['mil', 'penicillaria'],
                'sorgho': ['sorgho']
            }
            
            # Vérifier si des mots-clés correspondent
            for key, words in keywords.items():
                if any(word in message_lower for word in words):
                    print(f"    Mot-clé détecté: {key}")
                    # Essayer de trouver une réponse dans le dataset
                    for idx, row in chatbot_service.df.iterrows():
                        if any(word in row['question'].lower() for word in words):
                            answer = row['reponse']
                            if response_data.get('conseil'):
                                answer += f"\n\n **Conseil pratique** : {response_data['conseil']}"
                            return JsonResponse({"response": answer})
    
    else:
        print("   Service non prêt")
    
    # === 3. Fallback : réponses par défaut ===
    print("    Utilisation du fallback")
    
    # Réponses par défaut intelligentes basées sur le contenu
    if 'striga' in message_lower:
        defaults = [
            "Le striga est une mauvaise herbe parasite qui affecte les céréales. Pour la combattre: 1) Pratiquer la rotation des cultures, 2) Utiliser des variétés résistantes, 3) Labourer profondément avant la saison des pluies, 4) Semer à des dates optimales.",
            "Contre le striga: associer le maïs avec des légumineuses comme le niébé, utiliser du fumier bien décomposé, et pratiquer le désherbage manuel précoce.",
            "Le striga (Striga hermonthica) est un fléau pour les céréales. Solutions: semis précoce, utilisation de l'herbicide 2,4-D, et introduction de cultures pièges comme le coton."
        ]
    elif 'coton' in message_lower and any(word in message_lower for word in ['prix', 'cours', 'combien', 'valeur']):
        defaults = [
            "Le prix du coton au Burkina Faso varie selon la campagne. Actuellement, le prix garanti aux producteurs est d'environ 280 FCFA/kg pour le coton graine de première qualité.",
            "Pour la campagne 2023-2024, la SOFITEX propose 285 FCFA/kg pour le coton premier choix. Contactez votre union locale pour les prix exacts dans votre zone.",
            "Le cours du coton dépend de la qualité: 1ère qualité ~280-300 FCFA/kg, 2ème qualité ~250 FCFA/kg. Les prix sont fixés par la SOFITEX en début de campagne."
        ]
    elif 'fertilité' in message_lower or 'sol' in message_lower:
        defaults = [
            "Pour améliorer la fertilité naturellement: 1) Utiliser du compost ou du fumier, 2) Pratiquer la rotation cultures-céréales, 3) Planter des légumineuses comme engrais vert, 4) Maintenir une couverture végétale.",
            "Amélioration du sol: apport de matière organique, culture en couloirs avec acacia albida, paillage des résidus de récolte, et utilisation de la technique du zaï.",
            "La fertilité du sol s'améliore avec: le compostage, l'agroforesterie, les cultures associées, et la lutte contre l'érosion par des cordons pierreux."
        ]
    else:
        defaults = [
            "Je n'ai pas bien compris, mais je peux vous aider sur : prix des céréales, techniques de plantation, météo agricole, fertilisation, ou protection des cultures. Reformulez votre question !",
            "Posez-moi une question claire sur l'agriculture : coton, sol, maladies, crédit, variétés, irrigation...",
            "Dis-moi ton problème : sécheresse ? chenille ? striga ? prix ? sol dégradé ? Je connais tout ça !"
        ]
    
    return JsonResponse({"response": random.choice(defaults)})