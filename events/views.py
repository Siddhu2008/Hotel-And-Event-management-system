from django.shortcuts import render, redirect
from .models import Event, EventBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def event(request):
    events = Event.objects.all()

    if request.method == "POST":
        event_id = request.POST.get("event_id")  # match the input name in template
        number_of_guests = request.POST.get("guests")  # match the input name in template
        notes = request.POST.get("notes")  # optional notes

        if event_id and number_of_guests:
            booking = EventBooking.objects.create(
                user=request.user,
                event_id=event_id,
                is_confirmed=False,
            )
            # If you want to store number_of_guests and notes, add fields in EventBooking model
            booking.number_of_guests = number_of_guests
            booking.notes = notes
            booking.save()

            messages.success(request, f"Successfully booked {number_of_guests} spots for {booking.event.name}!")
            return redirect("event")
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, "event.html", {"events": events})

def adminEvent(request):
    events = Event.objects.all()
    return render(request, "AdminEvents.html", {"events": events})
