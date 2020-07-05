from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name='store-cart'),
    path('add/id=<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove/id=<int:id>', views.remove_from_cart, name='remove_from_cart'),
]