from django.utils.timezone import now
from rest_framework import serializers

from auth_app.models import CustomUser
       
class ProfileDetailSerializer(serializers.ModelSerializer):
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
            'email', 
            'uploaded_at', 
            'created_at'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        fields_never_null = [
            'first_name', 
            'last_name', 
            'location', 
            'tel', 
            'description', 
            'working_hours'
        ]
        
        for field in fields_never_null:
            if data.get(field) is None:
                data[field] = ""
                
        return data
    
    def update(self, instance, validated_data):
        if 'file' in validated_data:
            instance.uploaded_at = now()
        
        return super().update(instance, validated_data)
    