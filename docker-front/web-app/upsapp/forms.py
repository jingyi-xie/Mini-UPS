from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import ups_user

class UserSignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = ups_user
        fields = ['username', 'email', 'password1', 'password2']

