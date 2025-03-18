# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import timedelta
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    pass


User = get_user_model()


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # يمكن أن يكون رقمًا مكونًا من 6 أرقام مثلاً
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=10)  # صلاحية لمدة 10 دقائق
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Use get_or_create to ensure no duplicate is created
        UserProfile.objects.get_or_create(user=instance)
    else:
        # If needed, update the profile; otherwise, this may be optional
        if hasattr(instance, 'profile'):
            instance.profile.save()