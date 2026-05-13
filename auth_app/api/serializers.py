from rest_framework import serializers
from auth_app.models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .utils import get_auth_response

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, write_only=True)
    repeated_password = serializers.CharField(max_length=100, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if attrs['type'] not in [CustomUser.CUSTOMER, CustomUser.BUSINESS]:
            raise serializers.ValidationError("Invalid user type.")
        
        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return attrs
    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password is too short.")
        return value
        
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return get_auth_response(user, token)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(max_length=100, write_only=True)
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
    
        attrs['user'] = user
        return attrs
        
    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return get_auth_response(user, token)