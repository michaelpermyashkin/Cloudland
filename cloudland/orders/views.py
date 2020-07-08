import time
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from store.models import Product, Seller, Category
from carts.models import CartItem, Cart

from accounts.models import UserAddress, UserBillingAddress
from accounts.forms import UserAddressForm, UserBillingAddressForm

from .models import Order
from .utils import orderIdGenerator

try: 
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

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
        new_order.sub_total = cart.sub_total
        new_order.shipping = cart.shipping
        new_order.order_tax = round(cart.grand_total * Decimal(settings.DEFAULT_TAX_RATE), 2)
        new_order.order_total = cart.grand_total + new_order.order_tax
        new_order.order_id = orderIdGenerator()
        new_order.save()
    except:
        # Maybe an error message here
        return HttpResponseRedirect(reverse('store-cart'))
    # assign user to order
    new_order.user = request.user
    new_order.save()

    address_form = UserAddressForm()
    billing_form = UserBillingAddressForm()

    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserBillingAddress.objects.filter(user=request.user)

    # The payement form has been submitted - complete charge
    if request.method == 'POST':
        # Get user stipe id from the authenticated user model
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None
            pass
        # Add card to the customer
        if customer is not None:
            shipping_address = request.POST['shipping_address'] # an address ID
            billing_address = request.POST['billing_address'] # an address ID
            token = request.POST['stripeToken']
            card = customer.create_source(
                    customer.id,
                    source=token,
                )

            try:
                billing_address_instance = UserBillingAddress.objects.get(id=billing_address)
            except:
                billing_address_instance = None
            
            try:
                shipping_address_instance = UserAddress.objects.get(id=shipping_address)
            except:
                shipping_address_instance = None

            card.address_line1 = billing_address_instance.address or None
            card.address_line2 = billing_address_instance.address2 or None
            card.address_city = billing_address_instance.city or None
            card.address_state = billing_address_instance.state or None
            card.address_zip = billing_address_instance.zipcode or None
            card.save()

            charge_amount = int(new_order.order_total * 100)
            charge = stripe.Charge.create(
                    amount=charge_amount,
                    currency="usd",
                    source=card,
                    customer = customer,
                    description="Cloudland order #%s" %(new_order.order_id),
                )
            if charge["captured"]:
                new_order.status = 'Complete'
                new_order.shipping_address = shipping_address_instance
                new_order.billing_address = billing_address_instance
                new_order.order_receipt_link = charge["receipt_url"]
                new_order.save()
            # print(card)
            # print(charge)

    if new_order.status == 'Complete':
        cartID = request.session['cart_id'] 
        cart = Cart.objects.get(id=cartID)
        for item in cart.cartitem_set.all():
            item.product.quantity -= item.quantity
            item.product.total_purchases += item.quantity
            item.product.save()
            print("After: "+ str(item.product.quantity))
        del request.session['cart_id']
        del request.session['cart_items_total']
        return HttpResponseRedirect(reverse('accounts-dashboard'))


    context = {
        'order': new_order,
        'tax_rate': float(cart.grand_total) * settings.DEFAULT_TAX_RATE,
        'address_form': address_form,
        'billing_form': billing_form,
        'billing_addresses': billing_addresses,
        'current_addresses': current_addresses,
        'stripe_pub': stripe_pub,
    }
    return render(request, 'orders/checkout.html', context)

def billing(request):
    return render(request, 'orders/billing.html')