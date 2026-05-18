from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializers import OfferSerializer
from offer_app.models import Offer

class OfferPagination(PageNumberPagination):
    page_size = 6
    
class OfferListView(APIView):
    def get(self, request):
        paginator = OfferPagination()  
        queryset = Offer.objects.all()
        paginated_offers = paginator.paginate_queryset(queryset, request)
        serializer = OfferSerializer(paginated_offers, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

