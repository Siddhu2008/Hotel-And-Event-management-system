from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ContactMessage, UserProfile
from events.models import Event
from rooms.models import Room

def home(request):
    events = Event.objects.order_by('-id')[:3]  # Latest 3 events
    rooms = Room.objects.order_by('-id')[:3]    # Latest 3 rooms
    return render(request, 'home.html', {"events": events, "rooms": rooms})


# Contact Page View
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill out all fields.")

    return render(request, 'contact.html')


# Profile View (Requires Login)
@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update User Fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        # Update Profile Fields
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if phone:
            profile.phone = phone
        if address:
            profile.address = address
        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user, 'profile': profile})

# Profile View (Requires Login)
@login_required
def admin_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update User Fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        # Update Profile Fields
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if phone:
            profile.phone = phone
        if address:
            profile.address = address
        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('admin_profile')

    return render(request, 'Adminprofile.html', {'user': user, 'profile': profile})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rooms.models import RoomBooking
from events.models import EventBooking
from spas.models import SpaBooking
from dinings.models import DiningReservation

@login_required
def user_bookings(request):
    room_bookings = RoomBooking.objects.filter(user=request.user).select_related('room').order_by('-booking_date')
    event_bookings = EventBooking.objects.filter(user=request.user).select_related('event').order_by('-booking_datetime')
    spa_bookings = SpaBooking.objects.filter(user=request.user).select_related('service').order_by('-appointment_date', '-appointment_time')
    dining_bookings = DiningReservation.objects.filter(user=request.user).select_related('table').order_by('-reservation_date', '-reservation_time')

    context = {
        'room_bookings': room_bookings,
        'event_bookings': event_bookings,
        'spa_bookings': spa_bookings,
        'dining_bookings': dining_bookings,
    }
    return render(request, 'user_bookings.html', context)

