from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

class Seller(models.Model):
    seller_full_name = models.CharField(max_length=50)
    seller_listing_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.seller_listing_name


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30, help_text="Limit 30 characters")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(Category, help_text="Select the categories you would like the product to appear in")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description_short = models.CharField(max_length=50, default="", help_text="Limit 30 characters: Brief product description on item card")
    description_full = models.TextField(max_length=1000, default="", help_text="Your full item description when item details are viewed")
    product_image = models.ImageField(upload_to='product_images', help_text="Upload product image")
    is_featured = models.BooleanField(default=False)
    date_listed = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(help_text="Quantity available - Default 1", default=1)

    def __str__(self):
        return self.product_name
