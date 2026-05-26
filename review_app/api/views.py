from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ReviewSerializer
from .permissions import IsCustomer, IsReviewerAuthor
from review_app.models import Review

class ReviewListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]
    
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
    
    def post(self, request):  
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(reviewer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ReviewSingleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsReviewerAuthor()]
        return [IsAuthenticated()]
    
    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, review)
        
        serializer = ReviewSerializer(review, data=request.data, context={'request': request}, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)