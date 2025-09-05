"""
Django admin configuration for archives models.
"""

from django.contrib import admin

from .models import ArchiveItem


@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin):
    """Admin configuration for ArchiveItem model."""

    list_display = [
        'catalog_number', 'title', 'monastery', 'item_type',
        'material', 'condition', 'is_public', 'view_count'
    ]
    list_filter = [
        'monastery', 'item_type', 'material', 'condition',
        'is_public', 'language', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'catalog_number',
        'monastery__name', 'cultural_significance'
    ]
    autocomplete_fields = ['monastery']
    readonly_fields = ['view_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'monastery', 'title', 'description', 'item_type'
            )
        }),
        ('Cataloging', {
            'fields': (
                'catalog_number', 'acquisition_date', 'acquisition_method'
            )
        }),
        ('Historical Information', {
            'fields': (
                'estimated_age', 'historical_period', 'cultural_significance'
            )
        }),
        ('Physical Properties', {
            'fields': (
                'material', 'dimensions', 'weight', 'condition'
            )
        }),
        ('Language & Script', {
            'fields': (
                'language', 'script'
            ),
            'classes': ('collapse',)
        }),
        ('Digital Assets', {
            'fields': (
                'image', 'image_alt', 'additional_images',
                'scan', 'scan_resolution'
            )
        }),
        ('Access & Preservation', {
            'fields': (
                'is_public', 'requires_special_handling', 'preservation_notes'
            )
        }),
        ('Statistics', {
            'fields': (
                'view_count',
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('monastery')
