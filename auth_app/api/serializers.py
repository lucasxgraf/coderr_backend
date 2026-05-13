from rest_framework import serializers
from auth_app.models import CustomUser
from rest_framework.authtoken.models import Token

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
        
        if len(attrs['password']) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
        }