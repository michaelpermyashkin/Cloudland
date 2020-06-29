from django import forms
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import UsersLoginForm

def seller_dashboard(request):
    return render(request, 'sellers/dashboard.html')

def seller_login(request):
    if request.method == 'POST':
        form = UsersLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user.groups.filter(name='Seller').count():
                auth_login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('seller-dashboard'))
            else:
                messages.warning(request, "PERMISSION DENIED: Your account does not have the proper permission. If this is a mistake please contact us at cloudlandonline@gmail.com")
    # else render login page
    else:
        form = UsersLoginForm()
    return render(request, 'sellers/login.html', {'form': form})