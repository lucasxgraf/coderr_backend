from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileDetailSerializer
from auth_app.models import CustomUser
from .permissions import IsOwner

class ProfileBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.filter(type='business')
        serializer = ProfileDetailSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.filter(type='customer')
        serializer = ProfileDetailSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)
        
        serializer = ProfileDetailSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)