from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Min

from .serializers import OfferSerializer, OfferSingleSerializer, OfferPatchSerializer, OfferDetailSerializer
from .permissions import IsOfferOwner, IsBusinessUser
from offer_app.models import Offer, OfferDetail


class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return []

    def get_queryset(self):
        queryset = Offer.objects.all()

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            try:
                queryset = queryset.filter(user_id=int(creator_id))
            except ValueError:
                raise ValidationError({'error': 'Invalid creator_id'})

        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(details__price__gte=int(min_price))
            except ValueError:
                raise ValidationError({'error': 'Invalid min_price'})

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                queryset = queryset.filter(
                    details__delivery_time_in_days__lte=int(max_delivery_time)
                ).distinct()
            except ValueError:
                raise ValidationError({'error': 'Invalid max_delivery_time'})

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        queryset = queryset.annotate(min_price_val=Min('details__price'))
        ordering_map = {
            'min_price': 'min_price_val',
            '-min_price': '-min_price_val',
            'updated_at': 'updated_at',
            '-updated_at': '-updated_at',
        }
        ordering = self.request.query_params.get('ordering')
        if ordering in ordering_map:
            queryset = queryset.order_by(ordering_map[ordering])

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsOfferOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferPatchSerializer
        return OfferSingleSerializer

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class OfferDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer
    queryset = OfferDetail.objects.all()
