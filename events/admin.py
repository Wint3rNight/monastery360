"""
Django admin configuration for events models.
"""

from django.contrib import admin
from django.utils import timezone

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin configuration for Event model."""

    list_display = [
        'title', 'monastery', 'start_time', 'event_type',
        'is_public', 'status_display', 'is_featured'
    ]
    list_filter = [
        'monastery', 'event_type', 'is_public', 'is_featured',
        'recurrence_type', 'start_time', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'monastery__name',
        'location_details'
    ]
    autocomplete_fields = ['monastery']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_time'

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'monastery', 'title', 'description', 'short_description',
                'event_type'
            )
        }),
        ('Scheduling', {
            'fields': (
                'start_time', 'end_time', 'is_all_day',
                'location_details'
            )
        }),
        ('Recurrence', {
            'fields': (
                'recurrence_type', 'recurrence_end_date'
            ),
            'classes': ('collapse',)
        }),
        ('Visitor Information', {
            'fields': (
                'is_public', 'requires_registration', 'max_participants',
                'registration_deadline', 'entry_fee'
            )
        }),
        ('Event Details', {
            'fields': (
                'dress_code', 'language', 'special_instructions',
                'weather_dependent'
            ),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': (
                'contact_person', 'contact_phone', 'contact_email'
            ),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': (
                'image', 'image_alt'
            )
        }),
        ('Administrative', {
            'fields': (
                'is_featured', 'is_cancelled', 'cancellation_reason'
            )
        }),
        ('Statistics', {
            'fields': (
                'expected_attendance', 'actual_attendance'
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

    def status_display(self, obj):
        """Display the current status of the event."""
        status = obj.status
        if status == 'upcoming':
            return f"🟢 {status.title()}"
        elif status == 'ongoing':
            return f"🔵 {status.title()}"
        elif status == 'completed':
            return f"⚫ {status.title()}"
        elif status == 'cancelled':
            return f"🔴 {status.title()}"
        return status.title()

    status_display.short_description = 'Status'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('monastery')

    actions = ['mark_as_featured', 'mark_as_not_featured', 'cancel_events']

    def mark_as_featured(self, request, queryset):
        """Mark selected events as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} event(s) marked as featured.'
        )
    mark_as_featured.short_description = "Mark selected events as featured"

    def mark_as_not_featured(self, request, queryset):
        """Remove featured status from selected events."""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{updated} event(s) removed from featured.'
        )
    mark_as_not_featured.short_description = "Remove featured status"

    def cancel_events(self, request, queryset):
        """Cancel selected events."""
        updated = queryset.update(is_cancelled=True)
        self.message_user(
            request,
            f'{updated} event(s) cancelled.'
        )
    cancel_events.short_description = "Cancel selected events"
