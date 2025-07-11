from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


from user import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('my-listings/', views.my_listings, name='my_listings'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('top-donors/', views.top_donors, name='top_donors'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)