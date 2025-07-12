from django.urls import path

from listings import views

urlpatterns = [
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('favorites_list/<int:listing_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('interested_list/<int:listing_id>/', views.toggle_interest, name='toggle_interest'),
    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('', views.home, name='home'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('interested/', views.interested_list, name='interested_list'),
    path('my-listings/', views.my_listings, name='my_listings'),

]