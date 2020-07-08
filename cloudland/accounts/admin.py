from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserStripe
from accounts.forms import RegisterForm

admin.site.register(UserStripe)

class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


