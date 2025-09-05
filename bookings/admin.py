"""
Django admin configuration for bookings models.
"""

from django.contrib import admin
from django.utils import timezone

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for Booking model."""

    list_display = [
        'confirmation_number', 'name', 'monastery', 'visit_date',
        'number_of_visitors', 'status', 'visit_type', 'created_at'
    ]
    list_filter = [
        'monastery', 'status', 'visit_type', 'visit_date',
        'transportation_needed', 'accommodation_needed', 'created_at'
    ]
    search_fields = [
        'name', 'email', 'phone', 'confirmation_number',
        'monastery__name', 'organization'
    ]
    autocomplete_fields = ['monastery']
    readonly_fields = [
        'confirmation_number', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'visit_date'

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'confirmation_number', 'monastery', 'status'
            )
        }),
        ('Visitor Details', {
            'fields': (
                'name', 'email', 'phone', 'preferred_language'
            )
        }),
        ('Visit Information', {
            'fields': (
                'visit_date', 'visit_time', 'visit_type',
                'number_of_visitors', 'number_of_adults', 'number_of_children'
            )
        }),
        ('Group Information', {
            'fields': (
                'organization', 'group_leader'
            ),
            'classes': ('collapse',)
        }),
        ('Requirements', {
            'fields': (
                'special_requirements', 'purpose_of_visit',
                'transportation_needed', 'accommodation_needed'
            ),
            'classes': ('collapse',)
        }),
        ('Communication', {
            'fields': (
                'notes', 'admin_notes'
            )
        }),
        ('Follow-up', {
            'fields': (
                'confirmed_at', 'reminder_sent', 'feedback_requested'
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

    actions = [
        'confirm_bookings', 'cancel_bookings', 'mark_as_completed',
        'send_reminders'
    ]

    def confirm_bookings(self, request, queryset):
        """Confirm selected bookings."""
        now = timezone.now()
        updated = queryset.filter(status='pending').update(
            status='confirmed',
            confirmed_at=now
        )
        self.message_user(
            request,
            f'{updated} booking(s) confirmed.'
        )
    confirm_bookings.short_description = "Confirm selected bookings"

    def cancel_bookings(self, request, queryset):
        """Cancel selected bookings."""
        updated = queryset.exclude(status='completed').update(
            status='cancelled'
        )
        self.message_user(
            request,
            f'{updated} booking(s) cancelled.'
        )
    cancel_bookings.short_description = "Cancel selected bookings"

    def mark_as_completed(self, request, queryset):
        """Mark selected bookings as completed."""
        updated = queryset.filter(
            visit_date__lte=timezone.now().date()
        ).update(status='completed')
        self.message_user(
            request,
            f'{updated} booking(s) marked as completed.'
        )
    mark_as_completed.short_description = "Mark as completed"

    def send_reminders(self, request, queryset):
        """Mark selected bookings as having reminders sent."""
        updated = queryset.filter(
            status='confirmed',
            reminder_sent=False
        ).update(reminder_sent=True)
        self.message_user(
            request,
            f'Reminders marked as sent for {updated} booking(s).'
        )
    send_reminders.short_description = "Mark reminders as sent"
