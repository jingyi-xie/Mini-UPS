from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from upsapp.views import home_view, signup_view, list_view, pkg_detail_view, feedback_view, profile_update_view

app_name = 'upsapp'
urlpatterns = [
    path('', home_view, name = 'home'),
    path('signup/', signup_view, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='upsapp/logout.html'), name = 'logout'),
    path('login/', auth_views.LoginView.as_view(template_name='upsapp/login.html'), name = 'login'),
    path('update/', profile_update_view, name = 'update'),
    path('list/', list_view.as_view(), name = 'list'),
    path('pkg/<int:pk>/', pkg_detail_view.as_view(), name = 'detail'),
    path('feedback/', feedback_view.as_view(), name = 'feedback'),
]