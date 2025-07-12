# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('sifremi-unuttum/', views.password_reset_request_view, name='password_reset_request'),
    path('kodu-dogrula/', views.password_reset_verify_view, name='password_reset_verify'),
    path('sifre-belirle/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
