from django.db import models
from carts.models import Cart
from django.conf import settings
from accounts.models import UserAddress, UserBillingAddress

STATUS_CHOICES = (
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Complete', 'Complete'),
)

class Order(models.Model):
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, default=1)
    billing_address = models.ForeignKey(UserBillingAddress, on_delete=models.CASCADE, default=1)
    sub_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    shipping = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    order_tax = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    order_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    order_receipt_link = models.CharField(max_length=240, null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp_completed = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id

    def get_order_date(self):
        if self.address2:
            return '%s, %s, %s, %s, %s' % (self.address, self.address2, self.city, self.state, self.zipcode)
        else:
            return '%s, %s, %s, %s' % (self.address, self.city, self.state, self.zipcode)