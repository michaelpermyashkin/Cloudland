from django.contrib import admin
from django.urls import path, include
from . import views
from accounts import views as v

urlpatterns = [
    path('checkout/', views.checkout, name='orders-checkout'),
    path('billing/', views.billing, name='orders-billing'),
    path('ajax/add_user_address/', v.add_user_address, name='ajax-add-user-address'),
]