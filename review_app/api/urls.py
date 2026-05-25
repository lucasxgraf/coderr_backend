from django.urls import path
from .views import ReviewList

urlpatterns = [
    path('reviews/', ReviewList.as_view(), name='review-list'),
]