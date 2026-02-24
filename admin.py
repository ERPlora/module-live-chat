from django.contrib import admin

from .models import ChatConversation, ChatMessage

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'visitor_email', 'status', 'assigned_to', 'ended_at', 'created_at']
    search_fields = ['visitor_name', 'visitor_email', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender_type', 'sender_name', 'created_at']
    search_fields = ['sender_type', 'sender_name', 'message']
    readonly_fields = ['created_at', 'updated_at']

