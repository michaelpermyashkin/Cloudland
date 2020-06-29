from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.seller_dashboard, name='seller-dashboard'),
    path('login/', views.seller_login, name='seller-login'),
]