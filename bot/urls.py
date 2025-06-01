from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('', views.bot_chat_view, name='chat'),
    path('send/', views.send_message_view, name='send_message'),
    path('end/<int:conversation_id>/', views.end_conversation_view, name='end_conversation'),
    path('history/', views.conversation_history_view, name='history'),
]
