# serializers.py
import random
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Add a new field for the profile image; this field is optional.
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'profile_image')

    def create(self, validated_data):
        # Extract the image data if present
        profile_image = validated_data.pop('profile_image', None)
        # Create the user (using create_user to handle password hashing)
        user = User.objects.create_user(**validated_data)
        # Since we are using signals, the UserProfile should already exist.
        if profile_image:
            user.profile.image = profile_image
            user.profile.save()
        # Set inactive until email verification, and add a random verification code.
        user.is_active = False
        user.email_verification_code = str(random.randint(100000, 999999))
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('image',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'profile')
