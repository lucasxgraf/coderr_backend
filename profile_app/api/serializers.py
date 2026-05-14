from rest_framework import serializers
from auth_app.models import CustomUser

class ProfileBusinessSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at',
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type',
            'email',
            'created_at'
        ]

class ProfileCustomerSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at',
            'type',
            'email',
            'created_at'
        ]