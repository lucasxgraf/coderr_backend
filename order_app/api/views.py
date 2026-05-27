from django.db.models import Q

from rest_framework import generics, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.models import CustomUser
from offer_app.models import OfferDetail
from order_app.models import Order
from .permissions import IsCustomerUser, IsBusinessUser, IsAdminUser
from .serializers import OrderSerializer, OrderPatchSerializer


class OrderListView(generics.ListCreateAPIView):
    """List the current user's orders, or create a new order from an OfferDetail."""

    serializer_class = OrderSerializer
    pagination_class = None

    def get_permissions(self):
        """Require customer status for POST; any authenticated user can list."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Return orders where the current user is either the customer or the business side."""
        return Order.objects.filter(
            Q(business_user=self.request.user) | Q(customer_user=self.request.user)
        )

    def _get_offer_detail(self, offer_detail_id):
        """Return the OfferDetail for the given id, or None if missing/not found."""
        if offer_detail_id is None:
            return None, Response({'detail': 'Invalid request. Offer detail id is missing.'}, status=400)
        try:
            return OfferDetail.objects.get(pk=offer_detail_id), None
        except OfferDetail.DoesNotExist:
            return None, Response({'detail': 'OfferDetail not found.'}, status=404)
        except (ValueError, TypeError):
            return None, Response({'detail': 'Invalid offer_detail_id.'}, status=400)

    def _create_order_from_detail(self, offer_detail, customer):
        """Snapshot all OfferDetail fields into a new Order so future edits don't affect it."""
        return Order.objects.create(
            customer_user=customer,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress',
        )

    def create(self, request, *args, **kwargs):
        """Validate the offer_detail_id, create an order snapshot, and return it."""
        offer_detail, error = self._get_offer_detail(request.data.get('offer_detail_id'))
        if error:
            return error
        order = self._create_order_from_detail(offer_detail, request.user)
        return Response(self.get_serializer(order).data, status=201)


class OrderSingleView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """Patch the status of an order (business only) or delete it (admin only)."""

    queryset = Order.objects.all()

    def initial(self, request, *args, **kwargs):
        """Raise 404 before permission checks so non-existent orders never return 403."""
        if not Order.objects.filter(pk=kwargs.get('pk')).exists():
            raise NotFound()
        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        """Business users can patch status; only admins can delete."""
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def patch(self, request, *args, **kwargs):
        """Update order status and return the full order representation."""
        instance = self.get_object()
        serializer = OrderPatchSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Read response uses the full OrderSerializer, not the write-only patch serializer.
        return Response(OrderSerializer(instance).data)

    def delete(self, request, *args, **kwargs):
        """Delegate deletion to the DestroyModelMixin."""
        return self.destroy(request, *args, **kwargs)


class OrderCountView(generics.GenericAPIView):
    """Return the number of in-progress orders for a given business user."""

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'business_user_id'

    def get(self, request, *args, **kwargs):
        """Count and return active orders for the business user identified by the URL kwarg."""
        user = self.get_object()
        count = Order.objects.filter(business_user=user, status='in_progress').count()
        return Response({'order_count': count})


class CompletedOrderCountView(generics.GenericAPIView):
    """Return the number of completed orders for a given business user."""

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'business_user_id'

    def get(self, request, *args, **kwargs):
        """Count and return completed orders for the business user identified by the URL kwarg."""
        user = self.get_object()
        count = Order.objects.filter(business_user=user, status='completed').count()
        return Response({'completed_order_count': count})
