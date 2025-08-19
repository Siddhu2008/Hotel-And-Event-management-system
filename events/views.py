from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
import json
from django.utils.timezone import now
from django.db.models import Count, Q
from django.utils.timezone import localdate



# Define available time slots
TIME_SLOTS = [
    "10:00 AM", "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM", "08:00 PM"
]


@login_required
def event(request):
    events = Event.objects.annotate(
        bookings_today=Count(
            'eventbooking',
            filter=Q(eventbooking__booking_datetime__date=now().date())
        )
    )

    today = localdate()
    available_dates = [today + timedelta(days=i) for i in range(7)]

    if request.method == "POST":
        event_id = request.POST.get("event_id")
        number_of_guests = request.POST.get("guests")
        notes = request.POST.get("notes", "")
        selected_date = request.POST.get("booking_date")
        selected_time = request.POST.get("booking_time")

        if not (event_id and number_of_guests and selected_date and selected_time):
            messages.error(request, "Please fill in all required fields.")
            return redirect("event")

        try:
            number_of_guests = int(number_of_guests)
            if number_of_guests <= 0:
                messages.error(request, "Number of guests must be positive.")
                return redirect("event")
        except ValueError:
            messages.error(request, "Invalid number of guests.")
            return redirect("event")

        event_obj = get_object_or_404(Event, id=event_id)

        # Parse the selected date and time
        try:
            booking_datetime = datetime.strptime(
                f"{selected_date} {selected_time}", "%Y-%m-%d %I:%M %p"
            )
        except ValueError:
            messages.error(request, "Invalid date/time format.")
            return redirect("event")

        if booking_datetime < datetime.now():
            messages.error(request, "Cannot book a time slot in the past.")
            return redirect("event")

        # Capacity check
        total_booked = EventBooking.objects.filter(
            event=event_obj
        ).aggregate(total=Sum('number_of_guests'))['total'] or 0

        if total_booked + number_of_guests > event_obj.capacity:
            messages.error(request, "Not enough capacity for this event.")
            return redirect("event")

        # Check if selected slot is already booked
        existing_booking = EventBooking.objects.filter(
            event=event_obj,
            booking_datetime=booking_datetime
        ).exists()

        if existing_booking:
            messages.error(request, "This time slot is already booked.")
            return redirect("event")

        # Calculate total price
        total_price = event_obj.price_per_guest * number_of_guests

        # Create booking
        EventBooking.objects.create(
            user=request.user,
            event=event_obj,
            number_of_guests=number_of_guests,
            booking_datetime=booking_datetime,
            notes=notes,
            price=total_price,
            is_confirmed=False,
        )

        messages.success(request, f"Successfully booked {number_of_guests} guest(s) for {event_obj.name} at {selected_time}!")
        return redirect("event")
    context = {
        "events": events,
        "available_dates": available_dates,
    }
    return render(request, "event.html", context)


# AJAX endpoint to fetch available time slots

@login_required
def get_available_slots(request):
    if request.method == "GET":
        event_id = request.GET.get("event_id")
        date_str = request.GET.get("date")

        if not event_id or not date_str:
            return JsonResponse({"error": "Missing parameters"}, status=400)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Invalid event ID"}, status=404)

        try:
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Get already booked slots for this date
        booked_times = EventBooking.objects.filter(
            event=event,
            booking_datetime__date=booking_date
        ).values_list("booking_datetime", flat=True)

        booked_slots = [dt.strftime("%I:%M %p") for dt in booked_times]

        available_slots = [slot for slot in TIME_SLOTS if slot not in booked_slots]
        
        return JsonResponse({"slots": available_slots})


def adminEvent(request):
    events = Event.objects.all()
    return render(request, "AdminEvents.html", {"events": events})
