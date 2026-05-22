from django.urls import path
from .views import OrderListView, OrderSingleView, OrderCountView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderSingleView.as_view(), name='order-single'),
    path('order-count/<int:business_user_id>', OrderCountView.as_view(), name='order-count')
]