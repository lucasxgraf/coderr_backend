from rest_framework import serializers
from order_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'customer_user', 
            'business_user', 
            'title', 
            'revisions', 
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at', 
            'updated_at', 
        ]

class OrderPatchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = [
            'status'
        ]
        
    def validate_status(self, value):
        valid = ['in_progress', 'completed', 'cancelled']
        if value not in valid:
            raise serializers.ValidationError('Invalid status.')
        return value
