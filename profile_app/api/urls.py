from django.urls import path
from .views import ProfileBusinessView, ProfileCustomerView

urlpatterns = [
    path('business/', ProfileBusinessView.as_view(), name='business-profile'),
    path('customer/', ProfileCustomerView.as_view(), name='customer-profile')
]