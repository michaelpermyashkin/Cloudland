from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='orders-checkout'),
    path('billing/', views.billing, name='orders-billing'),
]