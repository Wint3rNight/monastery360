"""
Archives models for Monastery360.

This module defines models for digital preservation of historical items,
manuscripts, artifacts, and documents.
"""

from django.db import models
from django.urls import reverse

from core.models import Monastery


class ArchiveItem(models.Model):
    """
    Model for historical items in monastery archives.

    Supports manuscripts, artifacts, photographs, and other historical items
    with detailed metadata and digital preservation information.
    """

    ITEM_TYPES = [
        ('manuscript', 'Manuscript'),
        ('artifact', 'Artifact'),
        ('photograph', 'Photograph'),
        ('document', 'Document'),
        ('painting', 'Painting'),
        ('sculpture', 'Sculpture'),
        ('textile', 'Textile'),
        ('ritual_object', 'Ritual Object'),
        ('architectural', 'Architectural Element'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]

    MATERIAL_CHOICES = [
        ('paper', 'Paper'),
        ('parchment', 'Parchment'),
        ('palm_leaf', 'Palm Leaf'),
        ('wood', 'Wood'),
        ('metal', 'Metal'),
        ('stone', 'Stone'),
        ('textile', 'Textile'),
        ('clay', 'Clay'),
        ('bone', 'Bone'),
        ('mixed', 'Mixed Materials'),
        ('unknown', 'Unknown'),
    ]

    monastery = models.ForeignKey(
        Monastery,
        on_delete=models.CASCADE,
        related_name='archive_items',
        help_text="The monastery this item belongs to"
    )

    # Basic information
    title = models.CharField(
        max_length=300,
        help_text="Title or name of the archive item"
    )
    description = models.TextField(
        help_text="Detailed description of the item and its significance"
    )
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES,
        help_text="Type of archive item"
    )

    # Historical information
    estimated_age = models.CharField(
        max_length=100,
        blank=True,
        help_text="Estimated age or time period (e.g., '18th century', '200 years old')"
    )
    historical_period = models.CharField(
        max_length=100,
        blank=True,
        help_text="Historical period or dynasty"
    )
    cultural_significance = models.TextField(
        blank=True,
        help_text="Description of cultural and religious significance"
    )

    # Physical properties
    material = models.CharField(
        max_length=20,
        choices=MATERIAL_CHOICES,
        default='unknown',
        help_text="Primary material of the item"
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        help_text="Physical dimensions (e.g., '30cm x 20cm x 5cm')"
    )
    weight = models.CharField(
        max_length=50,
        blank=True,
        help_text="Weight of the item"
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='good',
        help_text="Current condition of the item"
    )

    # Digital preservation
    image = models.ImageField(
        upload_to='archives/images/',
        help_text="Main image of the archive item"
    )
    image_alt = models.CharField(
        max_length=200,
        help_text="Alt text for the main image (accessibility)"
    )

    # Additional images
    additional_images = models.JSONField(
        default=list,
        blank=True,
        help_text="List of additional image URLs"
    )

    # High-resolution scan for detailed viewing
    scan = models.FileField(
        upload_to='archives/scans/',
        blank=True,
        help_text="High-resolution scan or document file"
    )
    scan_resolution = models.CharField(
        max_length=50,
        blank=True,
        help_text="Resolution of the scan (e.g., '300 DPI')"
    )

    # Cataloging information
    catalog_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique catalog/inventory number"
    )
    acquisition_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when item was acquired by the monastery"
    )
    acquisition_method = models.CharField(
        max_length=100,
        blank=True,
        help_text="How the item was acquired (donated, purchased, etc.)"
    )

    # Language and script (for manuscripts)
    language = models.CharField(
        max_length=50,
        blank=True,
        help_text="Primary language (for manuscripts)"
    )
    script = models.CharField(
        max_length=50,
        blank=True,
        help_text="Script or writing system"
    )

    # Access and preservation
    is_public = models.BooleanField(
        default=True,
        help_text="Whether this item can be publicly viewed"
    )
    requires_special_handling = models.BooleanField(
        default=False,
        help_text="Whether item requires special preservation conditions"
    )
    preservation_notes = models.TextField(
        blank=True,
        help_text="Notes about preservation requirements and history"
    )

    # Usage tracking
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this item has been viewed"
    )
    download_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this item file has been downloaded"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['monastery', 'catalog_number']
        indexes = [
            models.Index(fields=['item_type']),
            models.Index(fields=['material']),
            models.Index(fields=['is_public']),
        ]

    def __str__(self):
        return f"{self.catalog_number}: {self.title}"

    def get_absolute_url(self):
        """Return the canonical URL for this archive item."""
        return reverse(
            'archives:item_detail',
            kwargs={
                'monastery_slug': self.monastery.slug,
                'catalog_number': self.catalog_number
            }
        )

    def increment_view_count(self):
        """Increment the view count for analytics."""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_download_count(self):
        """Increment the download count for analytics."""
        try:
            self.download_count += 1
            self.save(update_fields=['download_count'])
        except Exception:
            # best-effort: non-fatal if DB save fails
            pass

    @property
    def item_type_display_icon(self):
        """Return appropriate icon class for the item type."""
        icon_map = {
            'manuscript': 'fas fa-scroll',
            'artifact': 'fas fa-gem',
            'photograph': 'fas fa-camera',
            'document': 'fas fa-file-alt',
            'painting': 'fas fa-palette',
            'sculpture': 'fas fa-chess-rook',
            'textile': 'fas fa-tshirt',
            'ritual_object': 'fas fa-pray',
            'architectural': 'fas fa-building',
            'other': 'fas fa-question-circle',
        }
        return icon_map.get(self.item_type, 'fas fa-archive')

    @property
    def has_high_res_scan(self):
        """Check if this item has a high-resolution scan available."""
        return bool(self.scan)
