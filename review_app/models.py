from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    business_user = models.ForeignKey("auth_app.CustomUser", on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey("auth_app.CustomUser", on_delete=models.CASCADE, related_name='written_reviews')
    rating =  models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.business_user}"