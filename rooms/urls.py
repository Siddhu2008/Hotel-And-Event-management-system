from django.urls import path
from . import views

urlpatterns = [
    path('', views.room, name='room'),
    path('adminroom/', views.admin_room_bookings, name='adminRoom'),
    path('add/', views.add_room, name='add_room'),
   
]