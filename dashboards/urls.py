from django.urls import path
from . import views

urlpatterns = [
    path('adminDashboard/', views.AdminDashboard, name='AdminDashboard'),
    path('', views.UserDashboard, name='UserDashboard'),
    
   
]