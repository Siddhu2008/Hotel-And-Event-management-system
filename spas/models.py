from django.db import models
from accounts.models import User
# Create your models here.
class SpaService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_minutes = models.PositiveIntegerField(default=60)  # e.g., 60 for 1 hour
    def __str__(self):
        return self.name

class SpaBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
