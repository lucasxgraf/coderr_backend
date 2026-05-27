from django.db import models


class Offer(models.Model):
    """A service offer created by a business user, containing one or more detail tiers."""

    user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """A single pricing tier (basic / standard / premium) for an Offer."""

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Offer Detail'
        verbose_name_plural = 'Offer Details'

    def __str__(self):
        return f"{self.title} (Revisions: {self.revisions})"
