from django.urls import path
from .views import (
    RegisterView, LoginView, ManageUserView, VerifyEmailView,
    PasswordResetOTPRequestView, PasswordResetWithTokenView, OTPVerifyView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', ManageUserView.as_view(), name='manage-user'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('password-reset-otp-request/', PasswordResetOTPRequestView.as_view(), name='password-reset-otp-request'),
    path('password-reset-with-token/', PasswordResetWithTokenView.as_view(), name='password-reset-with-token'),
]
