from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('mark-messages-read/<str:username>/', views.mark_messages_read, name='mark_messages_read'),

]