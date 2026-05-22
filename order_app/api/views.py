from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import OrderSerializer, OrderPatchSerializer
from .permissions import IsCustomerUser, IsBusinessUser, IsAdminUser
from order_app.models import Order
from offer_app.models import OfferDetail
from auth_app.models import CustomUser

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
    
class OrderSingleView(APIView):
    def get_permissions(self):
            if self.request.method == 'PATCH':
                return [IsAuthenticated(), IsBusinessUser()]
            elif self.request.method == 'DELETE':
                return [IsAuthenticated(), IsAdminUser()]
            return [IsAuthenticated()]
    
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderPatchSerializer(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, business_user_id):
        try:
            user = CustomUser.objects.get(pk=business_user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        count = Order.objects.filter(business_user=user, status='in_progress').count()
        
        return Response({'order_count': count}, status=status.HTTP_200_OK)
    
class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, business_user_id):
        try:
            user = CustomUser.objects.get(pk=business_user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        count = Order.objects.filter(business_user=user, status='completed').count()
        
        return Response({'completed_order_count': count}, status=status.HTTP_200_OK)