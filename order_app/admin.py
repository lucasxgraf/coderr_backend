from django.contrib import admin

from order_app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin view for Order with status filtering and user search."""

    list_display = ('title', 'customer_user', 'business_user', 'status', 'price', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'customer_user__username', 'business_user__username')
