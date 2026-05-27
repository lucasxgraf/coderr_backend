from django.contrib import admin

from offer_app.models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """Inline editor for OfferDetail entries within the Offer admin view."""

    model = OfferDetail
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin view for Offer with inline detail tiers."""

    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    inlines = [OfferDetailInline]


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """Admin view for individual OfferDetail entries."""

    list_display = ('title', 'offer', 'offer_type', 'price', 'delivery_time_in_days', 'revisions')
    list_filter = ('offer_type',)
