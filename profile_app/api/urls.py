from django.urls import path

from .views import ProfileBusinessView, ProfileCustomerView, ProfileDetailView

urlpatterns = [
    path('profiles/business/', ProfileBusinessView.as_view(), name='business-profile'),
    path('profiles/customer/', ProfileCustomerView.as_view(), name='customer-profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]
