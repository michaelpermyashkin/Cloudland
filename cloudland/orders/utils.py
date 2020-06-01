import string
import random

from .models import Order

# Generates unique order ID
def orderIdGenerator(size=15, chars=string.ascii_uppercase+string.digits):
    newOrderId = ''.join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id = newOrderId)
        orderIdGenerator()
    except Order.DoesNotExist:
        return newOrderId