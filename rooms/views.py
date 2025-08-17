from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def room(request):
    rooms = Room.objects.all()

    if request.method == "POST":
        room_id = request.POST.get("room")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        if room_id and check_in and check_out:
            booking = RoomBooking.objects.create(
                user=request.user,
                room_id=room_id,
                check_in=check_in,
                check_out=check_out,
                is_confirmed=False
            )
            messages.success(request, f"Room {booking.room.room_number} booked successfully!")
            return redirect("room")
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, "room.html", {"rooms": rooms})


@login_required
def room_detail(request, room_id):  # ✅ match with urls.py
    room = get_object_or_404(Room, id=room_id) 
    if request.method == "POST":
        room_id = request.POST.get("room")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        if room_id and check_in and check_out:
            booking = RoomBooking.objects.create(
                user=request.user,
                room_id=room_id,
                check_in=check_in,
                check_out=check_out,
                is_confirmed=False
            )
            messages.success(request, f"Room {booking.room.room_number} booked successfully!")
            return redirect("room")
        else:
            messages.error(request, "Please fill all fields correctly.")
 # ✅ get by ID
    return render(request, 'room_detail.html', {'room': room})


def adminRoom(request):
    rooms = Room.objects.all()
    return render(request, "adminroom.html", {"rooms": rooms})
