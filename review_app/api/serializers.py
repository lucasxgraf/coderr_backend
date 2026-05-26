from rest_framework import serializers
from review_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]
        
    def validate(self, data):
        reviewer = self.context['request'].user
        business_user = data['business_user']
        
        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError("Fehlermeldung")
        return data 