from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminNotification, name='AdminNotification'),
 path('notifications/', views.notifications, name='notifications'),

    
   
]