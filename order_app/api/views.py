from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import OrderSerializer
from order_app.models import Order

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Order.objects.filter(Q(business_user=request.user) | Q(customer_user=request.user))
        
        serializer = OrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)