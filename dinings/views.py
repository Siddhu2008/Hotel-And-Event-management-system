from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Table, DiningReservation
from datetime import datetime


# Show available tables
def dinish(request):
    tables = Table.objects.all()
    return render(request, 'dinish.html', {'tables': tables})


# View single table (optional, not currently used in your template)
def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    return render(request, 'dinish.html', {'table': table})


# Book a table
@login_required
def book_table(request, table_id=None):
    if request.method == "POST":
        table_id = request.POST.get('table_id')
        reservation_date_str = request.POST.get('reservation_date')
        reservation_time_str = request.POST.get('reservation_time')

        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            messages.error(request, "Selected table does not exist.")
            return redirect('dinish')

        try:
            reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('dinish')

        try:
            reservation_time = datetime.strptime(reservation_time_str, "%H:%M").time()
        except (ValueError, TypeError):
            messages.error(request, "Invalid time format.")
            return redirect('dinish')

        # Prevent booking in the past
        now = timezone.localtime()
        if reservation_date < now.date() or (reservation_date == now.date() and reservation_time <= now.time()):
            messages.error(request, "Cannot book a table in the past.")
            return redirect('dinish')

        # Check for existing reservation (double booking prevention)
        already_booked = DiningReservation.objects.filter(
            table=table,
            reservation_date=reservation_date,
            reservation_time=reservation_time
        ).exists()

        if already_booked:
            messages.error(request, f"Table {table.table_number} is already booked at that time.")
            return redirect('dinish')

        # Create the reservation
        DiningReservation.objects.create(
            user=request.user,
            table=table,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            is_confirmed=True
        )

        messages.success(request, f"Your reservation for Table {table.table_number} has been submitted successfully.")
        return redirect('dinish')

    return redirect('dinish')


# Optional: User-specific reservation listing
@login_required
def my_dining_reservations(request):
    reservations = DiningReservation.objects.filter(user=request.user).order_by('-reservation_date', '-reservation_time')
    return render(request, 'dinish.html', {'reservations': reservations})

@login_required
def admin_dinish(request):
    reservations = DiningReservation.objects.select_related('user', 'table').order_by('-reservation_date', '-reservation_time')
    return render(request, 'admin_dinish.html', {'reservations': reservations})