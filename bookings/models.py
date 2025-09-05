"""
Bookings models for Monastery360.

This module defines models for visitor bookings and appointment scheduling.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import Monastery


class Booking(models.Model):
    """
    Model for visitor bookings and appointment scheduling.

    Allows visitors to schedule visits to monasteries with contact information
    and special requirements.
    """

    VISIT_TYPES = [
        ('general', 'General Visit'),
        ('guided_tour', 'Guided Tour'),
        ('meditation', 'Meditation Session'),
        ('photography', 'Photography Session'),
        ('research', 'Research/Academic'),
        ('group_visit', 'Group Visit'),
        ('special_event', 'Special Event'),
        ('volunteer', 'Volunteer Work'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]

    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="The monastery being visited"
    )

    # Visitor information
    name = models.CharField(
        max_length=100,
        help_text="Full name of the primary visitor"
    )
    email = models.EmailField(
        help_text="Email address for confirmation and communication"
    )
    phone = models.CharField(
        max_length=20,
        help_text="Contact phone number"
    )

    # Visit details
    visit_date = models.DateField(
        help_text="Preferred date for the visit"
    )
    visit_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Preferred time for the visit (if specific time needed)"
    )
    visit_type = models.CharField(
        max_length=20,
        choices=VISIT_TYPES,
        default='general',
        help_text="Type of visit requested"
    )

    number_of_visitors = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        default=1,
        help_text="Total number of people in the group"
    )
    number_of_adults = models.PositiveIntegerField(
        default=1,
        help_text="Number of adults in the group"
    )
    number_of_children = models.PositiveIntegerField(
        default=0,
        help_text="Number of children in the group"
    )

    # Additional information
    special_requirements = models.TextField(
        blank=True,
        help_text="Any special requirements or accessibility needs"
    )
    purpose_of_visit = models.TextField(
        blank=True,
        help_text="Purpose or reason for the visit"
    )
    preferred_language = models.CharField(
        max_length=50,
        default='English',
        help_text="Preferred language for communication"
    )

    # Group information (if applicable)
    organization = models.CharField(
        max_length=200,
        blank=True,
        help_text="Organization or institution name (if group visit)"
    )
    group_leader = models.CharField(
        max_length=100,
        blank=True,
        help_text="Group leader name (if different from primary contact)"
    )

    # Transportation and logistics
    transportation_needed = models.BooleanField(
        default=False,
        help_text="Whether transportation assistance is needed"
    )
    accommodation_needed = models.BooleanField(
        default=False,
        help_text="Whether accommodation recommendations are needed"
    )

    # Booking status and management
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the booking"
    )
    confirmation_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Unique confirmation number for the booking"
    )

    # Communication
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or comments"
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes for monastery staff"
    )

    # Follow-up
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the booking was confirmed"
    )
    reminder_sent = models.BooleanField(
        default=False,
        help_text="Whether a reminder has been sent"
    )
    feedback_requested = models.BooleanField(
        default=False,
        help_text="Whether feedback has been requested post-visit"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['visit_date']),
            models.Index(fields=['status']),
            models.Index(fields=['monastery', 'visit_date']),
        ]

    def __str__(self):
        return f"{self.name} - {self.monastery.name} on {self.visit_date}"

    def save(self, *args, **kwargs):
        """Generate confirmation number if not provided."""
        if not self.confirmation_number:
            # Generate a unique confirmation number
            import random
            import string
            while True:
                conf_num = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=8
                ))
                if not Booking.objects.filter(confirmation_number=conf_num).exists():
                    self.confirmation_number = conf_num
                    break
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the canonical URL for this booking."""
        return reverse(
            'bookings:booking_detail',
            kwargs={'confirmation_number': self.confirmation_number}
        )

    @property
    def is_upcoming(self):
        """Check if the visit is in the future."""
        return self.visit_date >= timezone.now().date()

    @property
    def is_today(self):
        """Check if the visit is today."""
        return self.visit_date == timezone.now().date()

    @property
    def is_past(self):
        """Check if the visit date has passed."""
        return self.visit_date < timezone.now().date()

    @property
    def days_until_visit(self):
        """Return the number of days until the visit."""
        if self.is_past:
            return 0
        delta = self.visit_date - timezone.now().date()
        return delta.days

    @property
    def needs_confirmation(self):
        """Check if the booking needs confirmation."""
        return self.status == 'pending'

    @property
    def visit_type_display_icon(self):
        """Return appropriate icon for the visit type."""
        icon_map = {
            'general': 'fas fa-eye',
            'guided_tour': 'fas fa-route',
            'meditation': 'fas fa-om',
            'photography': 'fas fa-camera',
            'research': 'fas fa-search',
            'group_visit': 'fas fa-users',
            'special_event': 'fas fa-star',
            'volunteer': 'fas fa-hands-helping',
            'other': 'fas fa-question-circle',
        }
        return icon_map.get(self.visit_type, 'fas fa-calendar-check')
