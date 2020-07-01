from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dasboard', views.seller_dashboard, name='seller-dashboard'),
    path('add-product/', views.add_product, name='add-product'),
    path('delete-product/pid=<int:id>', views.delete_product, name='delete-product'),
    path('edit/pid=<int:id>', views.edit_product, name='edit-product'),
    path('edit/bio=<slug:slug>', views.edit_bio, name='edit-bio'),
    path('login/', views.seller_login, name='seller-login'),
]