from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import OrderSerializer
from .permissions import IsCustomerUser
from order_app.models import Order
from offer_app.models import OfferDetail

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
    
    def get(self, request):
        queryset = Order.objects.filter(Q(business_user=request.user) | Q(customer_user=request.user))
        
        serializer = OrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        offer_detail_id = self.request.data.get('offer_detail_id')
        if offer_detail_id is None:
            return Response({'detail': 'Invalid request. Offer detail id is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            offer_detail = OfferDetail.objects.get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({'detail': 'OfferDetail not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        order = Order.objects.create(
            customer_user = request.user,
            business_user = offer_detail.offer.user,
            title = offer_detail.title,
            revisions = offer_detail.revisions,
            delivery_time_in_days = offer_detail.delivery_time_in_days,
            price = offer_detail.price,
            features = offer_detail.features,
            offer_type = offer_detail.offer_type,
            status = 'in_progress'
        )
        
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)