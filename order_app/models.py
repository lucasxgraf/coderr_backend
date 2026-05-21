from django.db import models

class Order(models.Model):
    customer_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='business_orders')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title