"""
Events models for Monastery360.

This module defines models for monastery events, festivals, and gatherings.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import Monastery


class Event(models.Model):
    """
    Model for monastery events, festivals, and public gatherings.

    Supports both recurring and one-time events with detailed scheduling
    and visitor information.
    """

    EVENT_TYPES = [
        ('festival', 'Festival'),
        ('ceremony', 'Religious Ceremony'),
        ('teaching', 'Teaching/Discourse'),
        ('meditation', 'Meditation Session'),
        ('celebration', 'Celebration'),
        ('pilgrimage', 'Pilgrimage'),
        ('cultural', 'Cultural Event'),
        ('educational', 'Educational Program'),
        ('maintenance', 'Maintenance/Closure'),
        ('other', 'Other'),
    ]

    RECURRENCE_TYPES = [
        ('none', 'No Recurrence'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('lunar', 'Based on Lunar Calendar'),
    ]

    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='events',
        help_text="The monastery hosting this event"
    )

    # Basic information
    title = models.CharField(
        max_length=200,
        help_text="Title of the event"
    )
    description = models.TextField(
        help_text="Detailed description of the event"
    )
    short_description = models.CharField(
        max_length=300,
        help_text="Brief description for previews and listings"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='other',
        help_text="Type of event"
    )

    # Scheduling
    start_time = models.DateTimeField(
        help_text="Start date and time of the event"
    )
    end_time = models.DateTimeField(
        help_text="End date and time of the event"
    )
    is_all_day = models.BooleanField(
        default=False,
        help_text="Whether this is an all-day event"
    )

    # Recurrence
    recurrence_type = models.CharField(
        max_length=20,
        choices=RECURRENCE_TYPES,
        default='none',
        help_text="How often this event recurs"
    )
    recurrence_end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last date for recurring events"
    )

    # Location within monastery
    location_details = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specific location within the monastery (e.g., 'Main Hall', 'Courtyard')"
    )

    # Visitor information
    is_public = models.BooleanField(
        default=True,
        help_text="Whether the public can attend this event"
    )
    requires_registration = models.BooleanField(
        default=False,
        help_text="Whether visitors need to register in advance"
    )
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of participants (if limited)"
    )
    registration_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Deadline for registration"
    )

    # Event details
    dress_code = models.CharField(
        max_length=200,
        blank=True,
        help_text="Dress code or special requirements"
    )
    entry_fee = models.CharField(
        max_length=100,
        default="Free",
        help_text="Entry fee or donation information"
    )
    language = models.CharField(
        max_length=100,
        default="Tibetan, English",
        help_text="Languages used during the event"
    )

    # Contact information
    contact_person = models.CharField(
        max_length=100,
        blank=True,
        help_text="Contact person for inquiries"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    contact_email = models.EmailField(
        blank=True,
        help_text="Contact email address"
    )

    # Media
    image = models.ImageField(
        upload_to='events/images/',
        blank=True,
        help_text="Event image or poster"
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for the event image (accessibility)"
    )

    # Additional information
    special_instructions = models.TextField(
        blank=True,
        help_text="Special instructions for attendees"
    )
    weather_dependent = models.BooleanField(
        default=False,
        help_text="Whether the event is weather dependent"
    )

    # Administrative
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this event on the homepage"
    )
    is_cancelled = models.BooleanField(
        default=False,
        help_text="Whether this event has been cancelled"
    )
    cancellation_reason = models.TextField(
        blank=True,
        help_text="Reason for cancellation (if applicable)"
    )

    # Statistics
    expected_attendance = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Expected number of attendees"
    )
    actual_attendance = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Actual number of attendees (post-event)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['event_type']),
            models.Index(fields=['is_public']),
            models.Index(fields=['monastery', 'start_time']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d')}"

    def get_absolute_url(self):
        """Return the canonical URL for this event."""
        return reverse(
            'events:event_detail',
            kwargs={
                'monastery_slug': self.monastery.slug,
                'event_id': self.id
            }
        )

    @property
    def is_upcoming(self):
        """Check if the event is in the future."""
        return self.start_time > timezone.now()

    @property
    def is_ongoing(self):
        """Check if the event is currently happening."""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def is_past(self):
        """Check if the event has ended."""
        return self.end_time < timezone.now()

    @property
    def duration_hours(self):
        """Return the duration of the event in hours."""
        if self.is_all_day:
            return 24
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600

    @property
    def status(self):
        """Return the current status of the event."""
        if self.is_cancelled:
            return 'cancelled'
        elif self.is_past:
            return 'completed'
        elif self.is_ongoing:
            return 'ongoing'
        else:
            return 'upcoming'

    @property
    def registration_open(self):
        """Check if registration is still open."""
        if not self.requires_registration:
            return False
        if self.registration_deadline:
            return timezone.now() < self.registration_deadline
        return self.is_upcoming
