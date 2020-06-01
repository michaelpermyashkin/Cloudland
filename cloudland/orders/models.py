from django.db import models
from carts.models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Complete', 'Complete'),
)

class Order(models.Model):
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    # Add address
    sub_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    shipping = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    order_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id