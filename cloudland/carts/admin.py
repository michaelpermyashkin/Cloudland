from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Cart
from .models import CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_total', 'shipping', 'grand_total')
admin.site.register(Cart, CartAdmin)
# admin.site.register(Cart)
# admin.site.register(CartItem)
