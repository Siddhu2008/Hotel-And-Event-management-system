from django.urls import path
from . import views

urlpatterns = [
    path('', views.room, name='room'),
     path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('adminroom/', views.adminRoom, name='adminRoom'),
    
   
]