
from django.db import models
from accounts.models import User  # Your custom user model

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # ✅ Added address
    account_type = models.CharField(max_length=50, default="Standard")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    member_since = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user.username