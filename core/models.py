"""
Core models for Monastery360.

This module defines the main Monastery model and related AudioPOI model
with location-based features (simplified for demo without GeoDjango).
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Monastery(models.Model):
    """
    Main model representing a monastery in Sikkim.

    Includes geographic location, basic information, and media.
    """

    name = models.CharField(
        max_length=200,
        help_text="Official name of the monastery"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        help_text="URL-friendly version of the name"
    )
    established_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(500),  # Earliest possible monastery
            MaxValueValidator(2024)  # Current year
        ],
        help_text="Year the monastery was established"
    )
    description = models.TextField(
        help_text="Detailed description of the monastery's history and significance"
    )
    short_description = models.CharField(
        max_length=500,
        help_text="Brief description for cards and previews"
    )

    # Location fields (simplified for demo)
    latitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate"
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate"
    )

    # Address information
    address = models.TextField(
        help_text="Full address of the monastery"
    )
    district = models.CharField(
        max_length=100,
        help_text="District in Sikkim"
    )
    altitude = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Altitude in meters above sea level"
    )

    # Media
    image = models.ImageField(
        upload_to='monasteries/images/',
        help_text="Main image of the monastery"
    )
    image_alt = models.CharField(
        max_length=200,
        help_text="Alt text for the main image (accessibility)"
    )

    # Contact and visiting information
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    email = models.EmailField(
        blank=True,
        help_text="Contact email address"
    )
    website = models.URLField(
        blank=True,
        help_text="Official website URL"
    )

    visiting_hours = models.CharField(
        max_length=200,
        default="6:00 AM - 6:00 PM",
        help_text="General visiting hours"
    )
    entry_fee = models.CharField(
        max_length=100,
        default="Free",
        help_text="Entry fee information"
    )

    # Metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the monastery is actively maintained"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether to feature this monastery on the homepage"
    )
    pano_id = models.CharField(
        max_length=100,
        help_text="ID used for panoramic view and React routing (matches JSON 'panoId')"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Monasteries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the canonical URL for this monastery."""
        return reverse('core:monastery_detail', kwargs={'slug': self.slug})


class AudioPOI(models.Model):
    """
    Audio Point of Interest model for guided audio tours.

    Represents specific locations within or around a monastery
    that have associated audio content.
    """

    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='audio_pois',
        help_text="The monastery this POI belongs to"
    )

    title = models.CharField(
        max_length=200,
        help_text="Title of this point of interest"
    )
    description = models.TextField(
        help_text="Description of what visitors will learn about"
    )

    # Location within the monastery grounds (simplified for demo)
    latitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate of this POI"
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate of this POI"
    )

    # Audio content
    audio_file = models.FileField(
        upload_to='audio/pois/',
        help_text="Audio file for this point of interest"
    )
    audio_duration = models.PositiveIntegerField(
        help_text="Duration of audio in seconds"
    )
    audio_transcript = models.TextField(
        blank=True,
        help_text="Text transcript of the audio (accessibility)"
    )

    # Display order and metadata
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order within the monastery tour"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this POI is active in tours"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['monastery', 'order', 'title']
        verbose_name = "Audio Point of Interest"
        verbose_name_plural = "Audio Points of Interest"

    def __str__(self):
        return f"{self.monastery.name} - {self.title}"

