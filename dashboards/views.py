from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now

from accounts.models import User
from rooms.models import RoomBooking
from events.models import EventBooking
from dinings.models import DiningReservation
from spas.models import SpaBooking
from .models import AdminStats

@staff_member_required
def admin_dashboard(request):
    # Generate real-time stats
    total_users = User.objects.count()
    total_room_bookings = RoomBooking.objects.count()
    total_event_bookings =EventBooking.objects.count()
    total_dining_bookings =DiningReservation.objects.count()
    total_spa_bookings =SpaBooking.objects.count()

    total_payments = 0  # Replace with actual logic if payments exist

    # Save a snapshot (optional)
    AdminStats.objects.create(
        total_users=total_users,
        total_room_bookings=total_room_bookings,
        total_event_bookings=total_event_bookings,
        total_dining_bookings=total_dining_bookings,
        total_spa_bookings=total_spa_bookings,
        total_payments=total_payments
    )

   
    context = {
        'total_users': total_users,
        'total_room_bookings': total_room_bookings,
        'total_event_bookings': total_event_bookings,
        'total_dining_bookings': total_dining_bookings,
        'total_spa_bookings': total_spa_bookings,

        'total_payments': total_payments,
       
    }

    return render(request, 'AdminDashboard.html', context)

