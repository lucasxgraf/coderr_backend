from django.utils.timezone import now

from rest_framework import serializers

from auth_app.models import CustomUser


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for reading and updating a user's public profile fields."""

    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'uploaded_at', 'created_at',
        ]

    def to_representation(self, instance):
        """Replace None with empty string for text profile fields to satisfy the API contract."""
        # AbstractUser ships first_name/last_name as blank strings, but custom
        # fields can be None in the DB — the API contract requires empty strings, never null.
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data.get(field) is None:
                data[field] = ""
        return data

    def update(self, instance, validated_data):
        """Stamp uploaded_at whenever the file field is included in the payload."""
        if 'file' in validated_data:
            instance.uploaded_at = now()
        return super().update(instance, validated_data)
