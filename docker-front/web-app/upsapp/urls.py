from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

app_name = 'upsapp'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='upsapp/login.html'), name = 'login'),
]