from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.AdminDashboard, name='AdminDashboard'),
    path('admin-booking/', views.AdminBooking, name='AdminBooking'),
    
   
]