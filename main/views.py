from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage 

def home(request):
    return render(request, 'home.html')


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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile

@login_required
def profile(request):
    user = request.user
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update user fields only if values are provided
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

        # Update profile fields only if values are provided
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
