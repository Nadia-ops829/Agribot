from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    # path('chatbot/status/', views.chatbot_status, name='chatbot_status'),
]