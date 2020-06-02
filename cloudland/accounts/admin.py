from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, UserAddressTable

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddressTable

admin.site.register(UserAddressTable, UserAddressAdmin)

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)
