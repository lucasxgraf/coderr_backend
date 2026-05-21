from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Min

from .serializers import OfferSerializer, OfferSingleSerializer, OfferPatchSerializer
from .permissions import IsOfferOwner
from offer_app.models import Offer

class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
class OfferListView(APIView):
    def get(self, request):
        paginator = OfferPagination()  
        queryset = Offer.objects.all()
        
        creator_id = request.query_params.get('creator_id')
        if creator_id:
            try:
                creator_id = int(creator_id)
            except ValueError:
                return Response({'error': 'Invalid creator_id'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(user_id=creator_id)
            
        min_price = request.query_params.get('min_price')
        if min_price:
            try:
                min_price = int(min_price)
            except ValueError:
                return Response({'error': 'Invalid min_price'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(details__price__gte=min_price)
            
        max_delivery_time = request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
            except ValueError:
                return Response({'error': 'Invalid max_delivery_time'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time).distinct()
            
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
            
        queryset = queryset.annotate(min_price_val=Min('details__price'))
        ordering = request.query_params.get('ordering')
        if ordering == 'min_price':
            queryset = queryset.order_by('min_price_val')
        elif ordering == '-min_price':
            queryset = queryset.order_by('-min_price_val')
        elif ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')
        elif ordering == '-updated_at':
            queryset = queryset.order_by('-updated_at')
        
        paginated_offers = paginator.paginate_queryset(queryset, request)
        serializer = OfferSerializer(paginated_offers, many=True, context={'request': request})
        
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Unauthorized. Please log in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.type != 'business':
            return Response({'detail': 'Forbidden. You have no permissions.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = OfferSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OfferSingleView(APIView):
    permission_classes = [IsAuthenticated, IsOfferOwner]

    def get(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSingleSerializer(offer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, offer)

        serializer = OfferPatchSerializer(offer, data=request.data, context={'request': request}, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
