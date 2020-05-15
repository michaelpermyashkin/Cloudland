from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from .forms import RegisterForm, UsersLoginForm
import store.urls 

# Signup
def register(request):
    #  create new user
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('store-home')
    # else they need to register
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login
def login(request):
    # Authenticate user login attempt
    if request.method == 'POST':
        form = UsersLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = password)
            auth_login(request, user)

        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('store-home')
    # else render login page
    else:
        form = UsersLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("store-home")