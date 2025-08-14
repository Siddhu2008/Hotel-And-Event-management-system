from django.db import models
from accounts.models import User

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.ManyToManyField(User)
