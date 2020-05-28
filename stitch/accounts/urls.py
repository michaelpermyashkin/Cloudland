from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='accounts-register'),
    path('login/', views.login, name='accounts-login'),
    path("logout", views.logout_request, name="accounts-logout"),
    path('dashboard/', views.dashboard, name='accounts-dashboard'),
]