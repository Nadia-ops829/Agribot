from django.shortcuts import render
from django.http import JsonResponse
from .tools.weather import get_temperature_ouagadougou

# Create your views here.


def chat_view(request):
    return render(request, 'index.html')

# Vue pour la temprature
def weather(request):
    temperature = get_temperature_ouagadougou()
    return JsonResponse({'temperature': temperature})

    
