from django.shortcuts import render

# Create your views here.
def event(request):
    return render(request, 'event.html')
def adminEvent(request):
    return render(request, 'AdminEvents.html')
