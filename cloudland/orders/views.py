import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from store.models import Product, Seller, Category
from carts.models import CartItem, Cart

from accounts.models import UserAddressTable
from accounts.forms import UserAddressForm

from .models import Order
from .utils import orderIdGenerator

@login_required
def checkout(request):
    # To checkout the cart must exist in the session, else redirect to cart page
    try:
        cartID = request.session['cart_id'] 
        cart = Cart.objects.get(id=cartID)
    except:
        cartID = None
        return HttpResponseRedirect(reverse('store-cart'))

    # If order exists we get the order, else create new order
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = orderIdGenerator()
        new_order.save()
    except:
        # Maybe an error message here
        return HttpResponseRedirect(reverse('store-cart'))

    try:
        address_added = request.GET['address_added']
    except:
        address_added = None
    
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    # assign user to order
    new_order.user = request.user
    new_order.save()

    if new_order.status == 'Complete':
        del request.session['cart_id']
        del request.session['cart_items_total']
        return HttpResponseRedirect(reverse('store-cart'))

    context = {
        'address_form': address_form,
    }
    return render(request, 'orders/checkout.html', context)

def billing(request):
    try:
        cartID = request.session['cart_id'] 
        cart = Cart.objects.get(id=cartID)
    except:
        cartID = None
        return HttpResponseRedirect(reverse('store-cart'))

    cart = Cart.objects.get(id=cartID) 
    args = {
        'cart': cart,
    }
    return render(request, 'orders/billing.html', args)