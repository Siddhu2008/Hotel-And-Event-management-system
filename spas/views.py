# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, time as dt_time
from .models import SpaBooking, SpaService


def spa(request):
    services = SpaService.objects.all()
    today = timezone.localdate()
    date_choices = [today + timedelta(days=i) for i in range(31)]

    selected_date_str = request.GET.get('date')
    selected_service_name = request.GET.get('service')

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else today
    except ValueError:
        selected_date = today

    try:
        selected_service = SpaService.objects.get(name=selected_service_name) if selected_service_name else services.first()
    except SpaService.DoesNotExist:
        selected_service = services.first()

    available_time_slots = []

    if selected_service:
        booked_times = SpaBooking.objects.filter(
            service=selected_service,
            appointment_date=selected_date
        ).values_list('appointment_time', flat=True)

        start_time = dt_time(9, 0)
        end_time = dt_time(18, 0)
        interval = timedelta(minutes=30)
        current_time = datetime.combine(selected_date, start_time)

        while current_time.time() <= end_time:
            if current_time.time() not in booked_times:
                available_time_slots.append(current_time.time())
            current_time += interval

    context = {
        'services': services,
        'date_choices': date_choices,
        'available_time_slots': available_time_slots,
        'selected_service': selected_service,
        'selected_date': selected_date,
    }

    return render(request, 'spa.html', context)


@login_required
def book_spa(request):
    if request.method == 'POST':
        service_name = request.POST.get('service')
        appointment_date_str = request.POST.get('date')
        appointment_time_str = request.POST.get('time')

        try:
            service = SpaService.objects.get(name=service_name)
        except SpaService.DoesNotExist:
            messages.error(request, 'Selected service does not exist.')
            return redirect('spa')

        try:
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date format.')
            return redirect('spa')

        try:
            appointment_time = datetime.strptime(appointment_time_str, '%H:%M:%S').time()
        except ValueError:
            try:
                appointment_time = datetime.strptime(appointment_time_str, '%H:%M').time()
            except ValueError:
                messages.error(request, 'Invalid time format.')
                return redirect('spa')

        if appointment_date < timezone.localdate():
            messages.error(request, 'Cannot book for past dates.')
            return redirect('spa')

        if SpaBooking.objects.filter(
            service=service,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            messages.error(request, 'Selected time slot is already booked.')
            return redirect('spa')

        SpaBooking.objects.create(
            user=request.user,
            service=service,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            is_confirmed=False
        )

        messages.success(request, 'Your spa booking has been submitted successfully.')
        return redirect('spa')

    return redirect('spa')


def get_available_slots(request):
    date_str = request.GET.get('date')
    service_name = request.GET.get('service')

    if not date_str or not service_name:
        return JsonResponse({'slots': []})

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        service = SpaService.objects.get(name=service_name)
    except (ValueError, SpaService.DoesNotExist):
        return JsonResponse({'slots': []})

    all_slots = [
        dt_time(10, 0),
        dt_time(11, 0),
        dt_time(12, 0),
        dt_time(14, 0),
        dt_time(15, 0),
        dt_time(16, 0),
    ]

    booked_times = SpaBooking.objects.filter(
        service=service,
        appointment_date=date_obj
    ).values_list('appointment_time', flat=True)

    # convert to string for comparison
    booked_str = [bt.strftime('%H:%M:%S') for bt in booked_times]
    available_slots = [slot.strftime('%H:%M:%S') for slot in all_slots if slot.strftime('%H:%M:%S') not in booked_str]

    return JsonResponse({'slots': available_slots})
