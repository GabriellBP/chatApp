from django.contrib.auth import logout
from django.urls import path
from . import views

urlpatterns = [
    # WEB
    # URL to index (login)
    path('', views.index, name='index'),
    # URL to register
    path('register', views.register_view, name='register'),
    # URL to chat listing users
    path('chat', views.chat_view, name='chats'),
    # URL to send and receive messages
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    # URL to logout
    path('logout', logout, {'next_page': 'index'}, name='logout'),

    # API:
    # URL form : "/api/messages/1/2"
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),  # For GET request.
    # URL form : "/api/messages/"
    path('api/messages/', views.message_list, name='message-list'),   # For POST
    # URL form "/api/users/1"
    path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    # URL form "/api/users/"
    path('api/users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
]