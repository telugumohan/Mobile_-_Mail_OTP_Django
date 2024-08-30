from django.db import models

class TempUser(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    email_otp = models.IntegerField()
    phone_otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
