import random
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import PasswordResetOTP

User = get_user_model()


class OTPService:
    """Service for handling OTP-related operations."""

    @staticmethod
    def generate_otp():
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def create_otp(user):
        otp = OTPService.generate_otp()
        PasswordResetOTP.objects.create(user=user, otp=otp)
        return otp

    @staticmethod
    def validate_otp(user, otp):
        try:
            otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp).latest('created_at')
            if otp_record.expires_at < timezone.now():
                raise ValueError("OTP has expired.")
            otp_record.delete()
            return True
        except PasswordResetOTP.DoesNotExist:
            raise ValueError("Invalid OTP.")

    @staticmethod
    def send_otp_email(user, subject, message):
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

