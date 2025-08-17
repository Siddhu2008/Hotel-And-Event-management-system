from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SpaService, SpaBooking

def spa(request):
    services = SpaService.objects.all()
    return render(request, 'spa.html', {'services': services})


@login_required
def book_spa(request):
    if request.method == 'POST':
        service_name = request.POST.get('service')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')

        try:
            service = SpaService.objects.get(name=service_name)
        except SpaService.DoesNotExist:
            messages.error(request, 'Selected service does not exist.')
            return redirect('spa')

        # Save booking
        booking = SpaBooking.objects.create(
            user=request.user,
            service=service,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            is_confirmed=False
        )
        messages.success(request, 'Your spa booking has been submitted successfully.')
        return redirect('spa')
    return redirect('spa')
