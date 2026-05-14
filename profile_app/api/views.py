from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import  ProfileBusinessSerializer, ProfileCustomerSerializer
from rest_framework.permissions import IsAuthenticated
from auth_app.models import CustomUser

class ProfileBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.filter(type='business')
        serializer = ProfileBusinessSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.filter(type='customer')
        serializer = ProfileCustomerSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)