from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products_page_all, name='store-products-page-all-home'),
    path('products/all/', views.products_page_all, name='store-products-page-all'),
    path('products/categories/', views.products_by_category, name='store-products-page-filter-category'),
    path('products/sellers/', views.products_by_seller, name='store-products-page-filter-seller'),
    path('products/price/', views.products_by_price, name='store-products-page-filter-price'),
    path('products/item#/', views.view_item, name='store-view-item'),
    path('contact/', views.contact, name='store-contact'),
]