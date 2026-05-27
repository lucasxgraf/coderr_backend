from django.contrib import admin

from review_app.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin view for Review with rating filter and user search."""

    list_display = ('reviewer', 'business_user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__username', 'business_user__username')
