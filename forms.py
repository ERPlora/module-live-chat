from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ChatConversation, ChatMessage

class ChatConversationForm(forms.ModelForm):
    class Meta:
        model = ChatConversation
        fields = ['visitor_name', 'visitor_email', 'status', 'assigned_to', 'ended_at', 'rating']
        widgets = {
            'visitor_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'visitor_email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'assigned_to': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'ended_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'rating': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['conversation', 'sender_type', 'sender_name', 'message']
        widgets = {
            'conversation': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'sender_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'sender_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'message': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

