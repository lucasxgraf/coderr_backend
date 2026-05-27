from django.db.models import Avg

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import CustomUser
from offer_app.models import Offer
from review_app.models import Review


class BaseInfoView(APIView):
    """Return platform-wide aggregate stats: review count, average rating, user count, offer count."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Compute and return the current platform statistics."""
        # aggregate() returns None when the table is empty; `or 0` guards against that.
        # float() cast ensures consistent JSON type regardless of DB backend.
        avg_rating = round(float(Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0), 1)
        data = {
            'review_count': int(Review.objects.count()),
            'average_rating': avg_rating,
            'business_profile_count': int(CustomUser.objects.filter(type='business').count()),
            'offer_count': int(Offer.objects.count()),
        }
        return Response(data, status=status.HTTP_200_OK)
