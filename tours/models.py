"""
Tours models for Monastery360.

This module defines models for virtual tours and panoramic experiences.
"""

from django.db import models
from django.urls import reverse

from core.models import Monastery


class Panorama(models.Model):
    """
    Model for 360-degree panoramic views of monastery locations.

    Supports virtual tours with narrated audio content.
    """

    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='panoramas',
        help_text="The monastery this panorama belongs to"
    )

    title = models.CharField(
        max_length=200,
        help_text="Title of this panoramic view"
    )
    description = models.TextField(
        help_text="Description of what this panorama shows"
    )

    # Location within monastery
    location_name = models.CharField(
        max_length=200,
        help_text="Name of the specific location (e.g., 'Main Hall', 'Courtyard')"
    )

    # 360-degree panoramic image
    image = models.ImageField(
        upload_to='tours/panoramas/',
        help_text="360-degree panoramic image file"
    )
    image_alt = models.CharField(
        max_length=200,
        help_text="Alt text for the panoramic image (accessibility)"
    )

    # Optional thumbnail for preview
    thumbnail = models.ImageField(
        upload_to='tours/thumbnails/',
        blank=True,
        help_text="Thumbnail image for preview"
    )

    # Narration audio
    narration_audio = models.FileField(
        upload_to='tours/audio/',
        blank=True,
        help_text="Audio narration for this panorama"
    )
    audio_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration of audio narration in seconds"
    )
    audio_transcript = models.TextField(
        blank=True,
        help_text="Text transcript of audio narration (accessibility)"
    )

    # Technical settings for panorama viewer
    initial_yaw = models.FloatField(
        default=0.0,
        help_text="Initial horizontal angle in degrees"
    )
    initial_pitch = models.FloatField(
        default=0.0,
        help_text="Initial vertical angle in degrees"
    )

    # Hotspots and navigation
    hotspots_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON data for interactive hotspots within the panorama"
    )

    # Display order and metadata
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order within the monastery tour"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this panorama"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this panorama is active"
    )

    # Usage statistics
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this panorama has been viewed"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['monastery', 'order', 'title']
        unique_together = ['monastery', 'location_name']

    def __str__(self):
        return f"{self.monastery.name} - {self.title}"

    def get_absolute_url(self):
        """Return the canonical URL for this panorama."""
        return reverse(
            'tours:panorama_detail',
            kwargs={
                'monastery_slug': self.monastery.slug,
                'panorama_id': self.id
            }
        )

    def increment_view_count(self):
        """Increment the view count for analytics."""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def has_audio(self):
        """Check if this panorama has audio narration."""
        return bool(self.narration_audio)

    @property
    def duration_formatted(self):
        """Return formatted audio duration (MM:SS)."""
        if not self.audio_duration:
            return "00:00"

        minutes = self.audio_duration // 60
        seconds = self.audio_duration % 60
        return f"{minutes:02d}:{seconds:02d}"
