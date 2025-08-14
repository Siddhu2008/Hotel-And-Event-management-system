from django.shortcuts import render

# Create your views here.
def AdminDashboard(request):
    return render(request, 'AdminDashboard.html')

def UserDashboard(request):
    return render(request, 'UserDashboard.html')

