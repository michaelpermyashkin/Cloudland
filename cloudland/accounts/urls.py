from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_request, name='accounts-register'),
    path('login/', views.login_request, name='accounts-login'),
    path("logout", views.logout_request, name="accounts-logout"),
    path('dashboard/', views.dashboard, name='accounts-dashboard'),
    path('activate/<str:activation_key>', views.email_activation, name='activation-view')
]