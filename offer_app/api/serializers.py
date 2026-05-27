from rest_framework import serializers

from offer_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Full serializer for a single OfferDetail tier."""

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer returning only the id and hypermedia URL for an OfferDetail."""

    url = serializers.HyperlinkedIdentityField(view_name='offer-detail-single', lookup_field='pk')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating Offers, including computed price/delivery fields."""

    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details',
        ]

    def get_min_price(self, obj):
        """Return the lowest price across all detail tiers, or None if no details exist."""
        if obj.details.exists():
            return min(detail.price for detail in obj.details.all())
        return None

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time across all detail tiers, or None if no details exist."""
        if obj.details.exists():
            return min(detail.delivery_time_in_days for detail in obj.details.all())
        return None

    def get_user_details(self, obj):
        """Return basic display info for the offer's creator."""
        if obj.user:
            return {
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'username': obj.user.username,
            }
        return None

    def validate_details(self, value):
        """Enforce that exactly 3 detail tiers (basic/standard/premium) are provided."""
        if len(value) != 3:
            raise serializers.ValidationError("Details have to be at least 3.")
        return value

    def create(self, validated_data):
        """Create the Offer and its nested OfferDetail tiers in a single operation."""
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


class OfferSingleSerializer(OfferSerializer):
    """Read serializer for a single Offer, returning minimal detail references instead of full data."""

    details = OfferDetailMinimalSerializer(many=True, read_only=True)


class OfferPatchSerializer(OfferSerializer):
    """Write serializer for partial Offer updates; matches details by offer_type instead of replacing them."""

    def validate_details(self, value):
        """Require offer_type on every detail so the update can identify which tier to patch."""
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError("offer_type is required to identify the detail.")
        return value

    def update(self, instance, validated_data):
        """Update top-level offer fields and patch each detail tier identified by offer_type."""
        details_data = validated_data.pop('details', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data['offer_type']
            try:
                detail = instance.details.get(offer_type=offer_type)
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()
            except OfferDetail.DoesNotExist:
                pass

        return instance
