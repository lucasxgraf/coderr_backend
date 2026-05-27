from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with profile and account type fields."""

    CUSTOMER = 'customer'
    BUSINESS = 'business'

    TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(max_length=255, blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    # Manually tracked because FileField provides no built-in upload timestamp.
    # Set in ProfileDetailSerializer.update() whenever `file` changes.
    uploaded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
