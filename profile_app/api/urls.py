from django.urls import path
from .views import ProfileBusinessView

urlpatterns = [
    path('business/', ProfileBusinessView.as_view(), name='business-profile'),
]