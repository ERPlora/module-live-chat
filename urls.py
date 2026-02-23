from django.urls import path
from . import views

app_name = 'live_chat'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('conversations/', views.conversations, name='conversations'),
    path('settings/', views.settings, name='settings'),
]
