from django.shortcuts import render

# Create your views here.
def room(request):
    return render(request, 'room.html')


def adminRoom(request):
    return render(request, 'AdminRooms.html')

