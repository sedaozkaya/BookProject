from django.urls import path

from listings import views

urlpatterns = [
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),

    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('', views.home, name='home'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('interested/', views.interested_list, name='interested_list'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:listing_id>/interest-and-message/', views.express_interest_and_message, name='interest_and_message'),
    path('listing/<int:listing_id>/toggle-interest/', views.toggle_interest, name='toggle_interest'),
    path('listing/<int:listing_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),




]