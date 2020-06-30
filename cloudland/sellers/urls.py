from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dasboard', views.seller_dashboard, name='seller-dashboard'),
    path('products/edit/pruduct_id=<int:id>/', views.edit_product, name='edit-product'),
    path('products/edit/seller=<slug:slug>/', views.edit_bio, name='edit-bio'),
    path('login/', views.seller_login, name='seller-login'),
]