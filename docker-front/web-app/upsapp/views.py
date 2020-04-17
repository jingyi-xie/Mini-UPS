from django.shortcuts import render, redirect
from .forms import UserSignupForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ups_user, ups_package, ups_truck
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.db.models import Q
from django.conf import settings

def home_view(request):
    qs = ups_package.objects.all()
    pkg_id = request.GET.get('pkgnum')
    if pkg_id != '':
        qs = qs.filter(
                Q(package_id = pkg_id)
            ).distinct()
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
def profile_view(request):
    return render(request, 'upsapp/profile.html')

# def get_pkg_queryset(query=None):
#     result = []
#     inputs = query.split("")
#     for q in inputs:
#         pkgs = ups_package.objects.filter(
#             Q(package_id = q)
#         ).distinct()

#         for pkg in pkgs:
#             result.append(pkg)
#     return list(set(result))

