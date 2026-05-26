from django.db.models import Avg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from review_app.models import Review
from auth_app.models import CustomUser
from offer_app.models import Offer

class BaseInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        data = {
            'review_count': int(Review.objects.count()),
            'average_rating': round(float(Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0), 1),
            'business_profile_count': int(CustomUser.objects.filter(type='business').count()),
            'offer_count': int(Offer.objects.count()),
        }
        
        return Response(data, status=status.HTTP_200_OK)