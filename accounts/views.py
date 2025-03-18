from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework import generics, status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .otp_service import OTPService

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user and send an OTP for verification."""
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Extract username and email from request data
        username = request.data.get('username')
        email = request.data.get('email')

        # Check if username already exists
        if username and User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already used."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email's already used."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with serializer validation and saving the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp = OTPService.create_otp(user)

        OTPService.send_otp_email(
            user,
            "Your Verification Password",
            f"Your verification password (OTP) is: {otp}. Use this code to activate your account."
        )

        return Response({
            "user": UserSerializer(user).data,
            "message": "Account created successfully. A verification password has been sent to your email."
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    """Verify the OTP to activate the user account."""

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        try:
            OTPService.validate_otp(user, otp)
            user.is_active = True
            user.save()
            return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"error": "Please verify your email first."}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key}, status=status.HTTP_200_OK)


class PasswordResetOTPRequestView(APIView):
    """Request a password reset OTP."""

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        otp = OTPService.create_otp(user)
        OTPService.send_otp_email(
            user, "Password Reset Verification Code",
            f"Your verification code is: {otp}. Please use this code to reset your password within 10 minutes."
        )
        return Response({"message": "Verification code has been sent to your email."}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    """Verify OTP for password reset."""

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({"error": "Email and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        try:
            OTPService.validate_otp(user, otp)
            signer = TimestampSigner()
            temp_token = signer.sign(user.pk)
            return Response({"temp_token": temp_token}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetWithTokenView(APIView):
    """Reset password using a temporary token."""

    def post(self, request):
        temp_token = request.data.get('temp_token')
        new_password = request.data.get('new_password')
        if not temp_token or not new_password:
            return Response({"error": "Temporary token and new password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        signer = TimestampSigner()
        try:
            user_pk = signer.unsign(temp_token, max_age=600)
            user = get_object_or_404(User, pk=user_pk)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except SignatureExpired:
            return Response({"error": "Temporary token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"error": "Invalid temporary token."}, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete the authenticated user's account."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        try:
            return self.request.user
        except User.DoesNotExist:
            raise NotFound("User not found.")
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Check if the request includes a profile image file
        profile_image = request.data.get('profile_image')
        if profile_image:
            # Assuming the user has a related UserProfile instance via a one-to-one relationship
            user_profile = instance.profile
            user_profile.image = profile_image
            user_profile.save()

        return Response({
            "message": "Profile updated successfully.",
            "user": serializer.data
        }, status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        """Handle user account deletion securely."""
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
