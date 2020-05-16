from django.contrib import admin

# Register your models here.
from .models import Product, Seller



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'seller', 'category', 'quantity', 'is_featured', 'description_short')
admin.site.register(Product, ProductAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display = ('seller_full_name', 'seller_listing_name', 'email', 'date_added')
admin.site.register(Seller, SellerAdmin)