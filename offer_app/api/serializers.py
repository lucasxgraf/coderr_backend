from rest_framework import serializers
from offer_app.models import Offer, OfferDetail
class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]  

class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetail-single', lookup_field='pk')

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'url'
        ]
        
class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Offer
        fields = [
            'id', 
            'user', 
            'title', 
            'image', 
            'description', 
            'created_at', 
            'updated_at', 
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
    
    def get_min_price(self, obj):
        if obj.details.exists():
            return min(detail.price for detail in obj.details.all())
        return None
    
    def get_min_delivery_time(self, obj):
        if obj.details.exists():
            return min(detail.delivery_time_in_days for detail in obj.details.all())
        return None
    
    def get_user_details(self, obj):
        if obj.user:
            return {
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'username': obj.user.username,
            }
        return None
    
    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Details have to be at least 3.")
        
        return value
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        
        offer = Offer.objects.create(**validated_data)
        
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer
    
class OfferSingleSerializer(OfferSerializer):
    details = OfferDetailMinimalSerializer(many=True, read_only=True)