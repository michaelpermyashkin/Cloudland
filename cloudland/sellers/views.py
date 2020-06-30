from django import forms
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import UsersLoginForm
from store.models import Product, Seller
from .forms import ProductEditForm, SellerBioEditForm

def seller_dashboard(request):
    seller = Seller.objects.get(seller=request.user)
    products = Product.objects.filter(seller=seller)
    args = {
        'products': products,
        'seller': seller,
    }
    return render(request, 'sellers/dashboard.html', args)

def edit_product(request, id):
    instance = get_object_or_404(Product, product_id=id)
    form = ProductEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('seller-dashboard'))
    args = {
        'form': form,
        'product': instance,
    }
    return render(request, 'sellers/product-edit.html', args)

def edit_bio(request, slug):
    seller = Seller.objects.get(seller=request.user)
    instance = get_object_or_404(Seller, slug=slug)
    form = SellerBioEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('seller-dashboard'))
    args = {
        'form': form,
        'seller': seller,
    }
    return render(request, 'sellers/seller-bio-edit.html', args)

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