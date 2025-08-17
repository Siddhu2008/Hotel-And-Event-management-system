from django.db import models
from accounts.models import User
# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # 🖼️ Image field

    def __str__(self):
        return f"Event {self.name} "


class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
