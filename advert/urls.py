from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('favorilerim/', views.favorites_list, name='favorites_list'),
    path('ilgilenilenler/', views.interested_list, name='interested_list'),
    path('profile/', views.profile_view, name='profile'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


