from django.db import models
from accounts.models import User
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField(default=50)
    price_per_guest = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def is_fully_booked_for_date(self, date):
        """
        Returns True if all slots are booked for a given date.
        """
        from .views import TIME_SLOTS  # Avoid circular import at top
        booked_slots = EventBooking.objects.filter(
            event=self, booking_datetime__date=date
        ).values_list("booking_datetime", flat=True)
        booked_time_strs = [dt.strftime("%I:%M %p") for dt in booked_slots]
        return all(slot in booked_time_strs for slot in TIME_SLOTS)


class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_guests = models.PositiveIntegerField()
    booking_datetime = models.DateTimeField(default=timezone.now)  # Selected date and time
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booking for {self.event.name} on {self.booking_datetime.strftime('%Y-%m-%d %I:%M %p')}"
