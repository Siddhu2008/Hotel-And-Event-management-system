from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),  
    path('event/', include('events.urls')), 
    path('dinish/', include('dinings.urls')),  
    path('dashboards/', include('dashboards.urls')),   
    path('notifications/', include('notifications.urls')),
    path('rooms/', include('rooms.urls')),
    path('spas/', include('spas.urls')),
     
    
]