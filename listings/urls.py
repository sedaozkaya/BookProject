from django.urls import path

from listings import views

urlpatterns = [
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('favorilerim/', views.favorites_list, name='favorites_list'),
    path('ilgilenilenler/', views.interested_list, name='interested_list'),
    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('', views.home, name='home'),
]