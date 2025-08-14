from django.db import models

# Create your models here.
class AdminStats(models.Model):
    date_generated = models.DateTimeField(auto_now_add=True)
    total_users = models.IntegerField()
    total_bookings = models.IntegerField()
    total_payments = models.DecimalField(max_digits=15, decimal_places=2)
