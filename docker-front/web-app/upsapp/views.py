from django.shortcuts import render, redirect
from .forms import UserSignupForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ups_user, ups_package, ups_truck
from django.views.generic import ListView, DetailView
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

class profile_view(LoginRequiredMixin, ListView):
    model = ups_package
    context_object_name = 'packages'
    template_name = 'upsapp/profile.html'
    def get_queryset(self):
        return ups_package.objects.filter(owner = self.request.user.user_name)

class pkg_detail_view(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ups_package
    def test_func(self):
        package = self.get_object()
        if self.request.user.user_name == package.owner:
            return True
        return False
