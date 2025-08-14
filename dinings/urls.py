from django.urls import path
from . import views

urlpatterns = [
    path('', views.dinish, name='dinish'),
   
]