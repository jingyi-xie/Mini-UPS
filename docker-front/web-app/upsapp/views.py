from django.shortcuts import render, redirect
from .forms import UserSignupForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ups_user, ups_package, ups_truck, ups_feedback
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Q
from django.conf import settings

def home_view(request):
    qs = ups_package.objects.all()
    pkg_id = request.GET.get('pkgnum')
    if pkg_id != '':
        qs = qs.filter(
                Q(package_id = pkg_id)
            ).distinct()
    else:
        qs = None
    context = {
        'queryset' : qs
    }
    return render(request, 'upsapp/home.html', context)

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

@login_required
def profile_update_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account profile updated!')
            return redirect('upsapp:home')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'upsapp/update.html', {'form': form}) 

class list_view(LoginRequiredMixin, ListView):
    model = ups_package
    context_object_name = 'packages'
    template_name = 'upsapp/list.html'
    def get_queryset(self):
        return ups_package.objects.filter(owner = self.request.user.username)

class pkg_detail_view(DetailView):
    model = ups_package

class feedback_view(SuccessMessageMixin, CreateView):
    model = ups_feedback
    fields = ['satisfied', 'content']
    template_name = 'upsapp/feedback.html'
    success_message = "Thanks for your feedback!"


