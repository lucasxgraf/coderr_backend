from django.urls import path
from .views import ProfileBusinessView, ProfileCustomerView, ProfileDetailView

urlpatterns = [
    path('business/', ProfileBusinessView.as_view(), name='business-profile'),
    path('customer/', ProfileCustomerView.as_view(), name='customer-profile'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]