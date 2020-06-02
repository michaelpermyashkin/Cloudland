import re
from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from carts.models import Cart
import store.urls 
from .forms import RegisterForm, UsersLoginForm
from .models import EmailConfirmed

from django.conf import settings

# Customer Dashboard
@login_required
def dashboard(request):
    try:
        cartID = request.session['cart_id'] 
        cart = Cart.objects.get(id=cartID)
    except:
        cartID = None

    if cartID != None:
        cart = Cart.objects.get(id=cartID) 
        args = {
            'cart': cart,
        }
        return render(request, 'accounts/dashboard.html', args)
    else:
        return render(request, 'accounts/dashboard.html')


# Signup
def register_request(request):
    #  create new user
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            messages.success(request, "Registration Successful! Please confirm your email now.")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')
    # else they need to register
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login
def login_request(request):
    # Authenticate user login attempt
    if request.method == 'POST':
        form = UsersLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            auth_login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')
    # else render login page
    else:
        form = UsersLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect(reverse('accounts-login'))


SHA1_RE = re.compile('^[a-f0-9]{40}$')
# Email activation view
def email_activation(request, activation_key):
    # Check if key is valid
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            raise Http404
        # Confirm the email
        if instance is not None and not instance.confirmed:
            page_message = 'Thank you! Your email has been confirmed!'
            context = {'page_message': page_message}
            instance.confirmed = True
            instance.activation_key = 'Confirmed'
            instance.save()
        # This email is already marked as being confirmed
        elif instance is not None and instance.confirmed:
            page_message = 'Your email has already been confirmed'
            context = {'page_message': page_message}
        else:
            page_message = None
            context = {}

        return render(request, 'accounts/activation-complete.html', context)
    # Raise 404 if invalid key
    else: 
        raise Http404