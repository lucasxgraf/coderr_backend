from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    """A customer review rating a business user, limited to one review per pair."""

    business_user = models.ForeignKey(
        "auth_app.CustomUser", on_delete=models.CASCADE, related_name='received_reviews'
    )
    reviewer = models.ForeignKey(
        "auth_app.CustomUser", on_delete=models.CASCADE, related_name='written_reviews'
    )
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = [('business_user', 'reviewer')]

    def __str__(self):
        return f"Review by {self.reviewer} for {self.business_user}"
