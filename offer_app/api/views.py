from django.db.models import Q, Min

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from offer_app.models import Offer, OfferDetail
from .permissions import IsOfferOwner, IsBusinessUser
from .serializers import OfferSerializer, OfferSingleSerializer, OfferPatchSerializer, OfferDetailSerializer


class OfferPagination(PageNumberPagination):
    """Pagination class that lets the client control page size via the page_size query param."""

    page_size_query_param = 'page_size'


class OfferListView(generics.ListCreateAPIView):
    """List all offers with optional filtering/ordering, or create a new offer (business users only)."""

    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    # Whitelist prevents arbitrary column injection via the ordering param.
    _ordering_map = {
        'min_price': 'min_price_val',
        '-min_price': '-min_price_val',
        'updated_at': 'updated_at',
        '-updated_at': '-updated_at',
    }

    def get_permissions(self):
        """Require authentication and business status for POST; no auth required for GET."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return []

    def _apply_creator_filter(self, qs, params):
        """Filter offers by creator user ID if creator_id is provided."""
        creator_id = params.get('creator_id')
        if not creator_id:
            return qs
        try:
            return qs.filter(user_id=int(creator_id))
        except ValueError:
            raise ValidationError({'error': 'Invalid creator_id'})

    def _apply_price_filter(self, qs, params):
        """Filter offers to those with at least one detail at or above min_price."""
        min_price = params.get('min_price')
        if not min_price:
            return qs
        try:
            return qs.filter(details__price__gte=int(min_price))
        except ValueError:
            raise ValidationError({'error': 'Invalid min_price'})

    def _apply_delivery_filter(self, qs, params):
        """Filter offers to those with at least one detail at or below max_delivery_time."""
        max_delivery = params.get('max_delivery_time')
        if not max_delivery:
            return qs
        try:
            return qs.filter(details__delivery_time_in_days__lte=int(max_delivery)).distinct()
        except ValueError:
            raise ValidationError({'error': 'Invalid max_delivery_time'})

    def _apply_search_filter(self, qs, params):
        """Filter offers by a case-insensitive search across title and description."""
        search = params.get('search')
        if search:
            return qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return qs

    def _apply_ordering(self, qs, params):
        """Annotate with min price and apply the requested ordering, defaulting to -updated_at."""
        # annotate() with aggregates can clear Meta ordering, so order_by is always explicit.
        qs = qs.annotate(min_price_val=Min('details__price'))
        ordering = params.get('ordering')
        if ordering in self._ordering_map:
            return qs.order_by(self._ordering_map[ordering])
        return qs.order_by('-updated_at')

    def get_queryset(self):
        """Build the filtered and ordered queryset from query params."""
        params = self.request.query_params
        qs = Offer.objects.all()
        qs = self._apply_creator_filter(qs, params)
        qs = self._apply_price_filter(qs, params)
        qs = self._apply_delivery_filter(qs, params)
        qs = self._apply_search_filter(qs, params)
        return self._apply_ordering(qs, params)

    def perform_create(self, serializer):
        """Attach the requesting user as the offer owner before saving."""
        serializer.save(user=self.request.user)


class OfferSingleView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, patch, or delete a single Offer; write access requires ownership."""

    queryset = Offer.objects.all()

    def get_serializer_class(self):
        """Use the patch serializer for PATCH requests, the read serializer otherwise."""
        if self.request.method == 'PATCH':
            return OfferPatchSerializer
        return OfferSingleSerializer

    def get_permissions(self):
        """Require ownership for mutating actions; any authenticated user can read."""
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """Force partial=True so PATCH never requires all fields to be present."""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class OfferDetailView(generics.RetrieveAPIView):
    """Retrieve a single OfferDetail tier by its primary key."""

    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer
    queryset = OfferDetail.objects.all()
