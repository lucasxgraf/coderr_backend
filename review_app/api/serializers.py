from rest_framework import serializers

from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for creating and reading reviews."""

    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def validate(self, data):
        """Prevent a customer from submitting a second review for the same business user."""
        # On PATCH without business_user in the payload, data.get('business_user') is None
        # and the duplicate check is silently skipped — this is intentional for updates.
        reviewer = self.context['request'].user
        business_user = data.get('business_user')
        if business_user and Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError('Error. Customer already reviewed business user.')
        return data
