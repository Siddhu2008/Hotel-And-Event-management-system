from django.db import models
from accounts.models import User
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100)  # e.g., 'Event', 'Room', 'Spa', 'Dining'
    related_id = models.PositiveIntegerField()  # Can store ID of booking
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)
