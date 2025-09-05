"""
Django admin configuration for tours models.
"""

from django.contrib import admin

from .models import Panorama


@admin.register(Panorama)
class PanoramaAdmin(admin.ModelAdmin):
    """Admin configuration for Panorama model."""

    list_display = [
        'title', 'monastery', 'location_name',
        'has_audio', 'view_count', 'is_featured', 'is_active'
    ]
    list_filter = [
        'monastery', 'is_featured', 'is_active', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'location_name',
        'monastery__name'
    ]
    autocomplete_fields = ['monastery']
    readonly_fields = [
        'view_count', 'created_at', 'updated_at'
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'monastery', 'title', 'description',
                'location_name', 'order'
            )
        }),
        ('Media', {
            'fields': (
                'image', 'image_alt', 'thumbnail'
            )
        }),
        ('Audio Narration', {
            'fields': (
                'narration_audio', 'audio_duration',
                'audio_transcript'
            ),
            'classes': ('collapse',)
        }),
        ('Panorama Settings', {
            'fields': (
                'initial_yaw', 'initial_pitch', 'hotspots_data'
            ),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': (
                'is_featured', 'is_active'
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

    def has_audio(self, obj):
        """Display whether panorama has audio narration."""
        return bool(obj.narration_audio)

    has_audio.boolean = True
    has_audio.short_description = 'Has Audio'
