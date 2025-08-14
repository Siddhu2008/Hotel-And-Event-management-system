from django.db import models
from accounts.models import User
# Create your models here.
class Table(models.Model):
    table_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

class DiningReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
