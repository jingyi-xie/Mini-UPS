from django.shortcuts import render, redirect
# from .forms import UserSignupForm, DriverInfoForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ups_user, ups_package, ups_truck
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

def signup_view(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully Sign Up!')
            return redirect('upsapp:login')
    else:
        form = UserSignupForm
    return render(request, 'upsapp/signup.html', {'form': form})

