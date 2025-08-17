from django.contrib import admin
from .models import SpaService, SpaBooking

@admin.register(SpaService)
class SpaServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']


@admin.register(SpaBooking)
class SpaBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'appointment_date', 'appointment_time', 'is_confirmed']
    list_filter = ['appointment_date', 'is_confirmed']
    search_fields = ['user__username', 'service__name']
