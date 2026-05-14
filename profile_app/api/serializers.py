from rest_framework import serializers
from auth_app.models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file', 
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type',
        ]