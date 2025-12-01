# chat/urls.py → Version finale propre
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    # On enlève la ligne weather/ car plus utilisée

]