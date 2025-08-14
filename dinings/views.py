from django.shortcuts import render

# Create your views here.
def dinish(request):
    return render(request, 'dinish.html')
