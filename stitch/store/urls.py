from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('products/', views.products_page, name='store-products-page'),
    path('products/item#/', views.view_item, name='store-view-item'),
    path('contact/', views.contact, name='store-contact'),
]