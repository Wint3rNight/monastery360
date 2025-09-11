"""
Core models for contact and feedback functionality.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ContactSubmission(models.Model):
    """Model for storing contact form submissions."""

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('booking', 'Booking Support'),
        ('technical', 'Technical Issue'),
        ('partnership', 'Partnership'),
        ('media', 'Media Inquiry'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()

    # Metadata
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_responded = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Feedback(models.Model):
    """Model for storing user feedback."""

    RATING_CHOICES = [
        (1, '⭐ Poor'),
        (2, '⭐⭐ Fair'),
        (3, '⭐⭐⭐ Good'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (5, '⭐⭐⭐⭐⭐ Excellent'),
    ]

    CATEGORY_CHOICES = [
        ('website', 'Website Experience'),
        ('content', 'Content Quality'),
        ('navigation', 'Navigation'),
        ('tours', 'Virtual Tours'),
        ('archives', 'Digital Archives'),
        ('booking', 'Booking Process'),
        ('mobile', 'Mobile Experience'),
        ('general', 'General Feedback'),
    ]

    # User information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    # Feedback content
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    # Additional context
    page_url = models.URLField(blank=True, help_text="URL of the page feedback is about")
    browser_info = models.CharField(max_length=500, blank=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=False, help_text="Show in testimonials")
    is_reviewed = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __str__(self):
        title = self.title or self.message[:50]
        return f"{self.name or 'Anonymous'} - {title} ({self.get_rating_display() if self.rating else 'No rating'})"

    def get_rating_stars(self):
        """Return rating as star string."""
        if self.rating:
            return '⭐' * self.rating
        return 'No rating'
