from django.urls import path

from .views import OfferListView, OfferSingleView, OfferDetailView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>', OfferSingleView.as_view(), name='offer-single'),
    path('offerdetails/<int:pk>', OfferDetailView.as_view(), name='offer-detail-single'),
]
