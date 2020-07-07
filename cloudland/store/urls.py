from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products_page_all, name='store-products-page-all-home'),
    path('products/all/', views.products_page_all, name='store-products-page-all'),
    path('c/<slug:slug>/', views.products_by_category, name='store-products-page-filter-category'),
    path('s/<slug:slug>/', views.products_by_seller, name='store-products-page-filter-seller'),
    path('products/v/item=<int:id>/', views.view_item, name='store-view-item'),
    path('contact/', views.contact, name='store-contact'),
    path('about/', views.about, name='about'),
]