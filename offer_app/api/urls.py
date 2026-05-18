from django.urls import path
from .views import OfferListView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offerdetails/<int:pk>', OfferListView.as_view(), name='offerdetail-single'),
]