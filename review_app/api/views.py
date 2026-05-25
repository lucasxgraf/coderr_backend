from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ReviewSerializer
from review_app.models import Review

class ReviewList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Review.objects.all()
        
        business_user_id = request.query_params.get('business_user_id')
        if business_user_id:
            try:
                business_user_id = int(business_user_id)
            except ValueError:
                return Response({'error': 'Invalid business_user_id'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(business_user_id=business_user_id)
            
        reviewer_id = request.query_params.get('reviewer_id')
        if reviewer_id:
            try:
                reviewer_id = int(reviewer_id)
            except ValueError:
                return Response({'error': 'Invalid reviewer_id'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(reviewer_id=reviewer_id)
            
        ordering = request.query_params.get('ordering')
        if ordering == 'rating':
            queryset = queryset.order_by('rating')
        elif ordering == '-rating':
            queryset = queryset.order_by('-rating')
        elif ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')
        elif ordering == '-updated_at':
            queryset = queryset.order_by('-updated_at')
        
        serializer = ReviewSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)