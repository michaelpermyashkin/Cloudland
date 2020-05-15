from django.contrib import admin

# Register your models here.
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'price', 'quantity', 'is_featured', 'description')
admin.site.register(Product, ProductAdmin)