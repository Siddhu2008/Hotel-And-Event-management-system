from django.shortcuts import render

# Create your views here.
def AdminNotification(request):
    return render(request, 'AdminNotification.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    # Get notifications for logged-in user
    user = request.user
    user_notifications = Notification.objects.filter(sent_to=user).order_by('-created_at')

    return render(request, 'notifications.html', {'notifications': user_notifications})
