from django.shortcuts import render

# Create your views here.
def AdminNotification(request):
    return render(request, 'AdminNotification.html')

