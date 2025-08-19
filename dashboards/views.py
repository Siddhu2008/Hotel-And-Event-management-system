from django.shortcuts import render
from .models import AdminStats

def AdminDashboard(request):
    # Get the latest stats entry
    stats = AdminStats.objects.order_by('-date_generated').first()
    return render(request, 'AdminDashboard.html', {'stats': stats})

def AdminBooking(request):
    return render(request, 'AdminBooking.html')