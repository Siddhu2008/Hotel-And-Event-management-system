from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def room(request):
    rooms = Room.objects.all()

    if request.method == "POST":
        room_id = request.POST.get("room")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        if room_id and check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                today = datetime.today().date()

                # Validate date logic
                if check_in_date < today or check_out_date <= check_in_date:
                    messages.error(request, "Invalid check-in/check-out dates.")
                    return redirect("room")

                # Check for overlapping bookings
                overlapping_bookings = RoomBooking.objects.filter(
                    room_id=room_id,
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date,
                )

                if overlapping_bookings.exists():
                    messages.error(request, "Room is already booked for the selected dates.")
                    return redirect("room")

                # Calculate nights and price
                nights = (check_out_date - check_in_date).days
                room = Room.objects.get(id=room_id)
                total_price = nights * room.price_per_night

                # Create the booking
                booking = RoomBooking.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in_date,
                    check_out=check_out_date,
                    is_confirmed=True,  # Assuming booking is confirmed immediately
                    total_price=total_price,
                )

                # Mark room as unavailable (optional: only if booking spans all availability)
                room.is_available = False
                room.save()

                messages.success(request, f"Room {room.room_number} booked for ₹{total_price}.")
                return redirect("room")

            except ValueError:
                messages.error(request, "Invalid date format.")
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, "room.html", {
        "rooms": rooms,
        "today": datetime.today().date()  # for date restrictions in template
    })


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                today = datetime.today().date()

                if check_in_date < today or check_out_date <= check_in_date:
                    messages.error(request, "Invalid check-in/check-out dates.")
                    return redirect("room_detail", room_id=room.id)

                overlapping_bookings = RoomBooking.objects.filter(
                    room=room,
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date,
                )

                if overlapping_bookings.exists():
                    messages.error(request, "Room is already booked for the selected dates.")
                    return redirect("room_detail", room_id=room.id)

                nights = (check_out_date - check_in_date).days
                total_price = nights * room.price_per_night

                booking = RoomBooking.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in_date,
                    check_out=check_out_date,
                    is_confirmed=False,
                    total_price=total_price,
                )

                messages.success(request, f"Room {room.room_number} booked for ₹{total_price}.")
                return redirect("room")

            except ValueError:
                messages.error(request, "Invalid date format.")
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, "room_detail.html", {'room': room})


def adminRoom(request):
    rooms = Room.objects.all()
    return render(request, "AdminRooms.html", {"rooms": rooms})
