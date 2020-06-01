from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products_page_all, name='store-products-page-all-home'),
    path('products/all/', views.products_page_all, name='store-products-page-all'),
    path('products/categories/<slug:slug>/', views.products_by_category, name='store-products-page-filter-category'),
    path('products/sellers/<slug:slug>/', views.products_by_seller, name='store-products-page-filter-seller'),
    path('products/order_by=<str:order_by>', views.products_order_by, name='store-products-order-by'),
    path('products/min_price=<int:min_price>&max_price=<int:max_price>/', views.products_by_price, name='store-products-page-filter-price'),
    path('products/min_price=<int:min_price>/', views.products_by_price_min, name='store-products-page-filter-price'),
    path('products/item/pruduct_id=<int:id>/', views.view_item, name='store-view-item'),
    path('contact/', views.contact, name='store-contact'),
    path('about/', views.about, name='about'),
]