from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser



class OTP(models.Model):
    identifier = models.CharField(max_length=255)  # ایمیل یا شماره موبایل
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)  # ۵ دقیقه اعتبار

class ParticipantStats(models.Model):
    major = models.CharField(max_length=100)  # رشته تحصیلی
    count = models.PositiveIntegerField(default=0)

class ParticipantCount(models.Model):
    total = models.PositiveIntegerField(default=0)


class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MajorStat(models.Model):
    major = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class MajorPopularity(models.Model):
    major = models.CharField(max_length=100, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.major} ({self.count})"

