from django.urls import path
from . import views

urlpatterns = [
    path('', views.event, name='event'),
    path('adminEvent/', views.admin_event_bookings, name='adminEvent'),
    path('get-available-slots/', views.get_available_slots, name='get_available_slots'),  
     path('add-event/', views.add_event, name='add_event'),
   
]