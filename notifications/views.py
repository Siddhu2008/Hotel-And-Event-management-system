from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    # Get notifications for logged-in user
    user = request.user
    user_notifications = Notification.objects.filter(sent_to=user).order_by('-created_at')

    return render(request, 'notifications.html', {'notifications': user_notifications})

@login_required
def AdminNotification(request):
    # Get notifications for the logged-in admin user
    user = request.user
    notifications = Notification.objects.filter(sent_to=user).order_by('-created_at')
    return render(request, 'AdminNotification.html', {'notifications': notifications})