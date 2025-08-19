from django.db import models
from accounts.models import User

class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class DiningReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('table', 'reservation_date', 'reservation_time')
        ordering = ['-reservation_date', '-reservation_time']

    def __str__(self):
        return f"Reservation for {self.user.username} - Table {self.table.table_number} on {self.reservation_date} at {self.reservation_time}"
