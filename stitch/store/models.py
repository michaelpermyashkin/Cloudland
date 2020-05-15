from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

# Create your models here.
class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=30)
    productImage = models.CharField(max_length=15)
    is_featured = models.BooleanField(default=False)
    dateListed = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.productName
