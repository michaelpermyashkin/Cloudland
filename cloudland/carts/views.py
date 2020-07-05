from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.conf import settings

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
def add_to_cart(request, id):
    request.session.set_expiry(31536000) # set to expire in 1 year
    try:
        session_ID = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        session_ID = request.session['cart_id']
    cart = Cart.objects.get(id=session_ID)

    # We try to add the product to the cart
    product = Product.objects.get(product_id=id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) # return tuple (<model object>, true/false)

    quantity = request.POST['selected_quantity']
    if cart_item.quantity + int(quantity) <= product.quantity:
        try:
            cart_item.quantity += int(quantity)
            cart_item.save()
        except:
            cart_item.quantity += 1
            cart_item.save()

        request.session['cart_items_total'] = cart.cartitem_set.count()
        calcCartTotal(cart)
        cart.save()
        return HttpResponseRedirect(reverse('store-cart'))
    else:
        messages.warning(request, "Unable to add this quantity to your cart because the quantity of this item in your cart will exceed the available stock.")
        return HttpResponseRedirect(reverse('store-cart'))


# handles removing a product to cart
def remove_from_cart(request, id):
    session_ID = request.session['cart_id']     
    cart = Cart.objects.get(id=session_ID)
    # We try to add the product to the cart
    product = Product.objects.get(product_id=id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) # return tuple (<model object>, true/false)
    
    cart_item.delete()
    request.session['cart_items_total'] = cart.cartitem_set.count()
    calcCartTotal(cart)
    cart.save()
    return HttpResponseRedirect(reverse('store-cart'))


# calculates cart total
def calcCartTotal(cart):
    newTotal = 0.00
    shippingTotal = 0.00
    for item in cart.cartitem_set.all():
        shippingTotal += float(item.product.shipping_cost)
        line_total = float(item.product.price) * item.quantity
        item.line_total = line_total
        item.save()
        newTotal += line_total
    cart.sub_total = newTotal
    cart.shipping = shippingTotal
    cart.grand_total = newTotal + shippingTotal
    cart.save()