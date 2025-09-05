"""
Tests for tours models and functionality.
"""

from django.test import TestCase

# from django.contrib.gis.geos import Point  # Disabled for demo
from django.urls import reverse

from core.models import Monastery
from tours.models import Panorama


class PanoramaModelTest(TestCase):
    """Test cases for Panorama model."""

    def setUp(self):
        """Set up test data."""
        self.monastery = Monastery.objects.create(
            name='Test Monastery',
            established_year=1800,
            description='A test monastery.',
            short_description='Test monastery.',
            latitude=27.3389,
            longitude=88.5937,
            address='Test Address',
            district='East Sikkim',
            image_alt='Test image',
        )

        self.panorama_data = {
            'monastery': self.monastery,
            'title': 'Main Hall Panorama',
            'description': '360-degree view of the main hall.',
            'location_name': 'Main Hall',
            'image_alt': 'Panoramic view of main hall',
            'audio_duration': 120,
        }

    def test_panorama_creation(self):
        """Test panorama creation."""
        panorama = Panorama.objects.create(**self.panorama_data)
        self.assertEqual(panorama.title, 'Main Hall Panorama')
        self.assertEqual(panorama.monastery, self.monastery)
        self.assertTrue(panorama.is_active)
        self.assertFalse(panorama.is_featured)

    def test_panorama_str_representation(self):
        """Test string representation."""
        panorama = Panorama.objects.create(**self.panorama_data)
        expected_str = f"{self.monastery.name} - Main Hall Panorama"
        self.assertEqual(str(panorama), expected_str)

    def test_has_audio_property(self):
        """Test has_audio property."""
        panorama = Panorama.objects.create(**self.panorama_data)
        self.assertFalse(panorama.has_audio)  # No audio file uploaded

    def test_duration_formatted(self):
        """Test formatted duration."""
        panorama = Panorama.objects.create(**self.panorama_data)
        self.assertEqual(panorama.duration_formatted, "02:00")

    def test_view_count_increment(self):
        """Test view count increment."""
        panorama = Panorama.objects.create(**self.panorama_data)
        initial_count = panorama.view_count
        panorama.increment_view_count()
        panorama.refresh_from_db()
        self.assertEqual(panorama.view_count, initial_count + 1)
