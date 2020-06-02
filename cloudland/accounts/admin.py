from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, UserAddress

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserAddress, UserAddressAdmin)

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)
