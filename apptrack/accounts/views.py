from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile or job application list
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')