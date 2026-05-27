from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_app.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin view for CustomUser with profile fields and type-based filtering."""

    list_display = ('username', 'email', 'type', 'is_staff', 'created_at')
    list_filter = ('type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('type', 'location', 'tel', 'description', 'working_hours', 'file')}),
    )
