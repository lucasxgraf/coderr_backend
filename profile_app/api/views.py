from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from auth_app.models import CustomUser
from .permissions import IsOwner
from .serializers import ProfileDetailSerializer


class ProfileBusinessView(generics.ListAPIView):
    """List all users with account type 'business'."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.filter(type='business')
    pagination_class = None


class ProfileCustomerView(generics.ListAPIView):
    """List all users with account type 'customer'."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.filter(type='customer')
    pagination_class = None


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve any profile, or update your own profile (PATCH/PUT require ownership)."""

    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        """Require ownership for write operations; any authenticated user can read."""
        if self.request.method in ('PATCH', 'PUT'):
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]
