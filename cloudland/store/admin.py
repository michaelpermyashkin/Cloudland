from django.contrib import admin

# Register your models here.
from .models import Product, Seller, Category, ProductReview

admin.site.site_header = "Cloudland Admininstration"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'seller', 'quantity', 'description_short')

admin.site.register(Product, ProductAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display = ('seller_full_name', 'seller_listing_name', 'email', 'date_added')
admin.site.register(Seller, SellerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

admin.site.register(ProductReview)