from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from review_app.models import Review
from .permissions import IsCustomer, IsReviewerAuthor
from .serializers import ReviewSerializer


class ReviewListView(generics.ListCreateAPIView):
    """List all reviews with optional filtering and ordering, or create a new review (customers only)."""

    serializer_class = ReviewSerializer
    pagination_class = None

    def get_permissions(self):
        """Require customer status for POST; any authenticated user can list."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def _apply_user_filters(self, qs, params):
        """Filter reviews by business_user_id and/or reviewer_id if provided."""
        business_user_id = params.get('business_user_id')
        if business_user_id:
            try:
                qs = qs.filter(business_user_id=int(business_user_id))
            except ValueError:
                return Review.objects.none()

        reviewer_id = params.get('reviewer_id')
        if reviewer_id:
            try:
                qs = qs.filter(reviewer_id=int(reviewer_id))
            except ValueError:
                return Review.objects.none()

        return qs

    def _apply_ordering(self, qs, params):
        """Apply the requested ordering if it is in the allowed whitelist."""
        ordering_map = {
            'rating': 'rating',
            '-rating': '-rating',
            'updated_at': 'updated_at',
            '-updated_at': '-updated_at',
        }
        ordering = params.get('ordering')
        if ordering in ordering_map:
            return qs.order_by(ordering_map[ordering])
        return qs

    def get_queryset(self):
        """Build the filtered and ordered queryset from query params."""
        params = self.request.query_params
        qs = Review.objects.all()
        qs = self._apply_user_filters(qs, params)
        return self._apply_ordering(qs, params)

    def perform_create(self, serializer):
        """Attach the requesting user as the reviewer before saving."""
        serializer.save(reviewer=self.request.user)


class ReviewSingleView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """Patch or delete a single review; both actions require the user to be the reviewer."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        """Require authorship for mutating actions; any authenticated user can read."""
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsReviewerAuthor()]
        return [IsAuthenticated()]

    def patch(self, request, *args, **kwargs):
        """Delegate partial update to the UpdateModelMixin."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delegate deletion to the DestroyModelMixin."""
        return self.destroy(request, *args, **kwargs)
