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
    selected_service_id = request.GET.get('service')  # changed to ID

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else today
    except ValueError:
        selected_date = today

    try:
        selected_service = SpaService.objects.get(id=selected_service_id) if selected_service_id else services.first()
    except (SpaService.DoesNotExist, ValueError):
        selected_service = services.first()

    time_slots = []

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
            is_booked = current_time.time() in booked_times
            time_slots.append({
                'time': current_time.time(),
                'is_booked': is_booked
            })
            current_time += interval

    context = {
        'services': services,
        'date_choices': date_choices,
        'time_slots': time_slots,
        'selected_service': selected_service,
        'selected_date': selected_date,
    }

    return render(request, 'spa.html', context)


@login_required
def book_spa(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')  # Changed from service_name
        appointment_date_str = request.POST.get('date')
        appointment_time_str = request.POST.get('time')

        try:
            service = SpaService.objects.get(id=service_id)  # Changed to use ID
        except (SpaService.DoesNotExist, ValueError):
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

        # Check if date is in the past
        if appointment_date < timezone.localdate():
            messages.error(request, 'Cannot book for past dates.')
            return redirect('spa')

        # Check if the time slot is already booked
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
            is_confirmed=True
        )

        messages.success(request, 'Your spa booking has been submitted successfully.')
        return redirect('spa')

    return redirect('spa')


def get_available_slots(request):
    date_str = request.GET.get('date')
    service_id = request.GET.get('service_id')

    print(f"Requested date: {date_str}, service ID: {service_id}")

    if not date_str or not service_id:
        return JsonResponse({'slots': [], 'error': 'Missing parameters'})

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        service = SpaService.objects.get(id=service_id)
    except (ValueError, SpaService.DoesNotExist) as e:
        print(f"Error: {e}")
        return JsonResponse({'slots': [], 'error': str(e)})

    # Generate slots from 09:00 to 18:00 in 30-minute intervals
    start_time = dt_time(9, 0)
    end_time = dt_time(18, 0)
    interval = timedelta(minutes=30)
    current_time = datetime.combine(date_obj, start_time)

    booked_times = SpaBooking.objects.filter(
        service=service,
        appointment_date=date_obj
    ).values_list('appointment_time', flat=True)

    slots = []
    while current_time.time() <= end_time:
        is_booked = current_time.time() in booked_times
        slots.append({
            'time': current_time.time().strftime('%H:%M:%S'),
            'is_booked': is_booked,
            'price': float(service.price)
        })
        current_time += interval

    print(f"Slots returned: {slots}")
    return JsonResponse({'slots': slots})
