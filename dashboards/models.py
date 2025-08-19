from django.db import models

# Create your models here.
class AdminStats(models.Model):
    date_generated = models.DateTimeField(auto_now_add=True)
    total_users = models.IntegerField(default=0)
    total_event_bookings = models.IntegerField(default=0)
    total_room_bookings = models.IntegerField(default=0)
    total_dining_bookings = models.IntegerField(default=0)
    total_spa_bookings = models.IntegerField(default=0)

    total_payments = models.DecimalField(max_digits=15, decimal_places=2,default=0.0)
    def __str__(self):
        return f"Stats on {self.date_generated.strftime('%Y-%m-%d %H:%M')}"
