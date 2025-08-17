
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dinish, name='dinish'),  # List all tables
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),  # Table details
    path('table/<int:table_id>/book/', views.book_table, name='book_table'),  # Book a table
    path('my-reservations/', views.my_dining_reservations, name='my_dining_reservations'),  # User reservations
]
