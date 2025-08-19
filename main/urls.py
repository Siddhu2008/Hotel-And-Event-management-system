from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
   path('profile/', views.profile, name='profile'),
   path('admin-profile/', views.admin_profile, name='admin_profile'),
   path('user-booking/', views.user_bookings, name='user_bookings'),

]