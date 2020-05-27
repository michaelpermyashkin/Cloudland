from django.shortcuts import render
from store.models import Product, Seller, Category
from carts.models import CartItem, Cart

def billing(request):
    try:
        session_ID = request.session['cart_id'] # session already active
    except:
        session_ID = None # no active session

    if session_ID != None:
        cart = Cart.objects.get(id=session_ID) 
        args = {
            'cart': cart,
        }
        return render(request, 'checkout/billing.html', args)
    else:
        # cart is empty so we load empty cart template
        return render(request, 'carts/cart.html')