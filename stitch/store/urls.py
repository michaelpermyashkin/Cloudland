from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products_page_all, name='store-products-page-all-home'),
    path('products/all/', views.products_page_all, name='store-products-page-all'),
    path('products/accessories/', views.products_page_accessories, name='store-products-page-accessories'),
    path('products/jewelry/', views.products_page_jewelry, name='store-products-page-jewelry'),
    path('products/craft/', views.products_page_craft, name='store-products-page-craft'),
    path('products/item#/', views.view_item, name='store-view-item'),
    path('contact/', views.contact, name='store-contact'),
]