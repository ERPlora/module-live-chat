from django.urls import path
from . import views

app_name = 'live_chat'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # ChatConversation
    path('chat_conversations/', views.chat_conversations_list, name='chat_conversations_list'),
    path('chat_conversations/add/', views.chat_conversation_add, name='chat_conversation_add'),
    path('chat_conversations/<uuid:pk>/edit/', views.chat_conversation_edit, name='chat_conversation_edit'),
    path('chat_conversations/<uuid:pk>/delete/', views.chat_conversation_delete, name='chat_conversation_delete'),
    path('chat_conversations/bulk/', views.chat_conversations_bulk_action, name='chat_conversations_bulk_action'),

    # ChatMessage
    path('chat_messages/', views.chat_messages_list, name='chat_messages_list'),
    path('chat_messages/add/', views.chat_message_add, name='chat_message_add'),
    path('chat_messages/<uuid:pk>/edit/', views.chat_message_edit, name='chat_message_edit'),
    path('chat_messages/<uuid:pk>/delete/', views.chat_message_delete, name='chat_message_delete'),
    path('chat_messages/bulk/', views.chat_messages_bulk_action, name='chat_messages_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
