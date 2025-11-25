from django.urls import path
from . import views

# URL patterns for the chat app

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('weather/', views.weather, name='weather'),
]