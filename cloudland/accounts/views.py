from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UsersLoginForm
from carts.models import Cart
import store.urls 


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
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = password)
            auth_login(request, user)
            # user.emailconfirmed.activate_user_email()
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
    messages.info(request, "Logged out successfully!")
    return redirect("/")