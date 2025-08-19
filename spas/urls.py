# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.spa, name='spa'),
    path('book/', views.book_spa, name='book_spa'),
  path('slots/', views.get_available_slots, name='spa_slots'),
]
