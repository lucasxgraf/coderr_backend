from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(generics.GenericAPIView):
    """Create a new user account and return an authentication token."""

    serializer_class = RegistrationSerializer

    def post(self, request):
        """Validate registration data, save the user, and return token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Authenticate a user by username and password and return a token."""

    serializer_class = LoginSerializer

    def post(self, request):
        """Validate credentials and return the user's auth token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response(user_data, status=status.HTTP_200_OK)
