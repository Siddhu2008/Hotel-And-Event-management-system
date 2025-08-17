from django.shortcuts import render

# Create your views here.
def dinish(request):
    return render(request, 'dinish.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Table, DiningReservation

# Display all available tables
def dinish(request):
    tables = Table.objects.all()
    return render(request, 'dinish.html', {'tables': tables})

# View details of a single table
def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    return render(request, 'dinish.html', {'table': table})

# Make a reservation for a table
@login_required
def book_table(request, table_id=None):
    if request.method == "POST":
        table_id = request.POST.get('table_id')
        table = get_object_or_404(Table, id=table_id)
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')

        if reservation_date and reservation_time:
            DiningReservation.objects.create(
                user=request.user,
                table=table,
                reservation_date=reservation_date,
                reservation_time=reservation_time
            )
            messages.success(request, f'Your reservation for Table {table.table_number} has been submitted!')
            return redirect('dinish')
        else:
            messages.error(request, 'Please provide both date and time for your reservation.')
    return redirect('dinish')

 # Optional: List all reservations of the logged-in user
@login_required
def my_dining_reservations(request):
    reservations = DiningReservation.objects.filter(user=request.user)
    return render(request, 'dinish.html', {'reservations': reservations})
