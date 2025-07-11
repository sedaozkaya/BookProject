from django.urls import path

from messaging import views

urlpatterns = [
    path('listing/<int:listing_id>/message/', views.start_conversation, name='start_conversation'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/', views.my_conversations, name='my_conversations'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),]