from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileDetailSerializer
from auth_app.models import CustomUser
from .permissions import IsOwner


class ProfileBusinessView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.filter(type='business')
    pagination_class = None


class ProfileCustomerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.filter(type='customer')
    pagination_class = None


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT'):
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]
