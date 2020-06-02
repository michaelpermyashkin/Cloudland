from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse

from store.models import Product # Product model
from carts.models import Cart # Cart Model
from carts.models import CartItem

# Shopping Cart
def cart(request):
    try:
        session_ID = request.session['cart_id'] # session already active
    except:
        session_ID = None # no active session

    if session_ID != None:
        cart = Cart.objects.get(id=session_ID) 
        args = {
            'cart': cart,
        }
        return render(request, 'carts/cart.html', args)
    else:
        # cart is empty so we load empty cart template
        return render(request, 'carts/cart.html')
    

# handles adding a product to cart
def add_to_cart(request):
    request.session.set_expiry(31536000) # set to expire in 1 year
    try:
        session_ID = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        session_ID = request.session['cart_id']
    cart = Cart.objects.get(id=session_ID)

    selectedProductID = None
    for key in request.POST.keys():
        if key.startswith('get-prod-info'):
            selectedProductID = int(key[13:])

    # We try to add the product to the cart
    product = Product.objects.get(product_id=selectedProductID)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) # return tuple (<model object>, true/false)

    try:
        quantity_selected = request.POST['selected_quantity']
        cart_item.quantity += int(quantity_selected)
        cart_item.save()
    except:
        cart_item.quantity = 1
        cart_item.save()

    request.session['cart_items_total'] = cart.cartitem_set.count()
    calcCartTotal(cart)
    cart.save()
    return HttpResponseRedirect(reverse('store-cart'))


# handles removing a product to cart
def remove_from_cart(request):
    selectedProductID = None
    for key in request.POST.keys():
        if key.startswith('get-prod-info'):
            selectedProductID = int(key[13:])

    session_ID = request.session['cart_id']     
    cart = Cart.objects.get(id=session_ID)
    # We try to add the product to the cart
    product = Product.objects.get(product_id=selectedProductID)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) # return tuple (<model object>, true/false)
    
    cart_item.delete()
    request.session['cart_items_total'] = cart.cartitem_set.count()
    calcCartTotal(cart)
    cart.save()
    return HttpResponseRedirect(reverse('store-cart'))


# calculates cart total
def calcCartTotal(cart):
    newTotal = 0.00
    for item in cart.cartitem_set.all():
        line_total = float(item.product.price) * item.quantity
        item.line_total = line_total
        item.save()
        newTotal += line_total
    cart.total = newTotal
    cart.save()