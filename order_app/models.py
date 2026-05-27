from django.db import models

STATUS_CHOICES = [
    ('in_progress', 'in_progress'),
    ('completed', 'completed'),
    ('cancelled', 'cancelled'),
]


class Order(models.Model):
    """A placed order created from an OfferDetail snapshot at booking time."""

    customer_user = models.ForeignKey(
        'auth_app.CustomUser', on_delete=models.CASCADE, related_name='customer_orders'
    )
    business_user = models.ForeignKey(
        'auth_app.CustomUser', on_delete=models.CASCADE, related_name='business_orders'
    )
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
