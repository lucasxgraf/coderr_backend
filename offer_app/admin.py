from django.contrib import admin

from offer_app.models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    inlines = [OfferDetailInline]


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer', 'offer_type', 'price', 'delivery_time_in_days', 'revisions')
    list_filter = ('offer_type',)
