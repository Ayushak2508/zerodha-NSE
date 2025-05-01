from django.db import models
from django.contrib.auth.models import User

class loginfrom(models.Model):
    email = models.EmailField()
    phone = models.IntegerField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)

