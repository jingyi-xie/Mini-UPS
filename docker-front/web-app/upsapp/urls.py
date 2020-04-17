from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from upsapp.views import home_view, signup_view, profile_view, pkg_detail_view

app_name = 'upsapp'
urlpatterns = [
    path('', home_view, name = 'home'),
    path('signup/', signup_view, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='upsapp/logout.html'), name = 'logout'),
    path('login/', auth_views.LoginView.as_view(template_name='upsapp/login.html'), name = 'login'),
    path('profile/', profile_view.as_view(), name = 'profile'),
    path('pkg/<int:pk>/', pkg_detail_view.as_view(), name = 'detail'),
]