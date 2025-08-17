from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

# ✅ Add media serving (only works in DEBUG mode / development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
