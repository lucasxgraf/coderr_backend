from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from .utils import get_auth_response


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration input and create a new user account."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, write_only=True)
    repeated_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, attrs):
        """Ensure passwords match, user type is valid, and email is not already taken."""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if attrs['type'] not in [CustomUser.CUSTOMER, CustomUser.BUSINESS]:
            raise serializers.ValidationError("Invalid user type.")

        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists.")

        return attrs

    def validate_password(self, value):
        """Enforce a minimum password length of 6 characters."""
        # Django's AUTH_PASSWORD_VALIDATORS are NOT triggered here — they only
        # run via django.contrib.auth.password_validation, not DRF serializers.
        if len(value) < 6:
            raise serializers.ValidationError("Password is too short.")
        return value

    def create(self, validated_data):
        """Create the user and return an auth response dict with token."""
        # repeated_password is a validation-only field; create_user() rejects unknown kwargs.
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return get_auth_response(user, token)


class LoginSerializer(serializers.Serializer):
    """Validate username/password credentials and return the authenticated user."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        """Authenticate the user and attach the user object to attrs."""
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))

        if not user:
            raise serializers.ValidationError('Invalid username or password.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """Retrieve or create a token and return the auth response dict."""
        user = validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return get_auth_response(user, token)
