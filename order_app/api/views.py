from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .serializers import OrderSerializer, OrderPatchSerializer
from .permissions import IsCustomerUser, IsBusinessUser, IsAdminUser
from order_app.models import Order
from offer_app.models import OfferDetail
from auth_app.models import CustomUser


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Order.objects.filter(
            Q(business_user=self.request.user) | Q(customer_user=self.request.user)
        )

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')
        if offer_detail_id is None:
            return Response(
                {'detail': 'Invalid request. Offer detail id is missing.'},
                status=400
            )

        try:
            offer_detail = OfferDetail.objects.get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({'detail': 'OfferDetail not found.'}, status=404)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress',
        )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=201)


class OrderSingleView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderPatchSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(instance).data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'business_user_id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        count = Order.objects.filter(business_user=user, status='in_progress').count()
        return Response({'order_count': count})


class CompletedOrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'business_user_id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        count = Order.objects.filter(business_user=user, status='completed').count()
        return Response({'completed_order_count': count})
