from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsReviewerAuthor
from review_app.models import Review


class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            try:
                queryset = queryset.filter(business_user_id=int(business_user_id))
            except ValueError:
                return Review.objects.none()

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            try:
                queryset = queryset.filter(reviewer_id=int(reviewer_id))
            except ValueError:
                return Review.objects.none()

        ordering = self.request.query_params.get('ordering')
        ordering_map = {
            'rating': 'rating',
            '-rating': '-rating',
            'updated_at': 'updated_at',
            '-updated_at': '-updated_at',
        }
        if ordering in ordering_map:
            queryset = queryset.order_by(ordering_map[ordering])

        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewSingleView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsReviewerAuthor()]
        return [IsAuthenticated()]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
