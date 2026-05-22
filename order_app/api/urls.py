from django.urls import path
from .views import OrderListView, OrderSingleView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderSingleView.as_view(), name='order-single'),
]