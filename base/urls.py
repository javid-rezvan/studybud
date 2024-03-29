from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logouUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('topics/',views.topics,name='topics'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('user-profile/<str:pk>/',views.userProfile,name='profile'),
    path('edit-user/',views.updateUser,name='edit-user'),
   
]
