from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.+
class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=13)
    gender = models.CharField(max_length=3, choices=(('M',"male"),('f',"female"),('o',"other"),('N/A',"don't want to mention")))
    user = models.CharField(max_length=1, choices=(
        ("s","supplier"),
        ("c","customer")
    ))

class Address(models.Model):
    title = models. CharField(max_length=40)
    Address_line_one = models.CharField(max_length=50)
    Address_line_two = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    pincode = models.IntegerField()
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING)