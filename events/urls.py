from django.urls import path
from . import views

urlpatterns = [
    path('', views.event, name='event'),
    path('adminEvent/', views.adminEvent, name='adminEvent'),
     path('event/<int:room_id>/', views.event_detail, name='event_detail'),
    
   
]