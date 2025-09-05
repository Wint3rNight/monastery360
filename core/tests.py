"""
Tests for core models and functionality.
"""

# from django.contrib.gis.geos import Point  # Disabled for demo
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from core.models import AudioPOI, Monastery


class MonasteryModelTest(TestCase):
    """Test cases for Monastery model."""

    def setUp(self):
        """Set up test data."""
        self.monastery_data = {
            'name': 'Test Monastery',
            'established_year': 1800,
            'description': 'A test monastery for unit testing.',
            'short_description': 'Test monastery.',
            'latitude': 27.3389,  # Gangtok coordinates
            'longitude': 88.5937,
            'address': 'Test Address, Gangtok, Sikkim',
            'district': 'East Sikkim',
            'image_alt': 'Test monastery image',
        }

    def test_monastery_creation(self):
        """Test monastery creation."""
        monastery = Monastery.objects.create(**self.monastery_data)
        self.assertEqual(monastery.name, 'Test Monastery')
        self.assertEqual(monastery.established_year, 1800)
        self.assertTrue(monastery.is_active)
        self.assertFalse(monastery.is_featured)

    def test_monastery_slug_generation(self):
        """Test automatic slug generation."""
        monastery = Monastery.objects.create(**self.monastery_data)
        self.assertEqual(monastery.slug, 'test-monastery')

    def test_monastery_str_representation(self):
        """Test string representation."""
        monastery = Monastery.objects.create(**self.monastery_data)
        self.assertEqual(str(monastery), 'Test Monastery')

    def test_monastery_coordinates(self):
        """Test coordinate properties."""
        monastery = Monastery.objects.create(**self.monastery_data)
        self.assertAlmostEqual(monastery.latitude, 27.3389, places=4)
        self.assertAlmostEqual(monastery.longitude, 88.5937, places=4)

    def test_monastery_absolute_url(self):
        """Test get_absolute_url method."""
        monastery = Monastery.objects.create(**self.monastery_data)
        expected_url = reverse('core:monastery_detail', kwargs={'slug': monastery.slug})
        self.assertEqual(monastery.get_absolute_url(), expected_url)

    def test_invalid_established_year(self):
        """Test validation for established year."""
        self.monastery_data['established_year'] = 2030  # Future year
        monastery = Monastery(**self.monastery_data)
        with self.assertRaises(ValidationError):
            monastery.full_clean()


class AudioPOIModelTest(TestCase):
    """Test cases for AudioPOI model."""

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

        self.poi_data = {
            'monastery': self.monastery,
            'title': 'Main Hall',
            'description': 'The main prayer hall of the monastery.',
            'latitude': 27.3390,
            'longitude': 88.5938,
            'audio_duration': 180,
        }

    def test_audio_poi_creation(self):
        """Test AudioPOI creation."""
        poi = AudioPOI.objects.create(**self.poi_data)
        self.assertEqual(poi.title, 'Main Hall')
        self.assertEqual(poi.monastery, self.monastery)
        self.assertEqual(poi.audio_duration, 180)
        self.assertTrue(poi.is_active)

    def test_audio_poi_str_representation(self):
        """Test string representation."""
        poi = AudioPOI.objects.create(**self.poi_data)
        expected_str = f"{self.monastery.name} - Main Hall"
        self.assertEqual(str(poi), expected_str)

    def test_audio_poi_coordinates(self):
        """Test coordinate properties."""
        poi = AudioPOI.objects.create(**self.poi_data)
        self.assertAlmostEqual(poi.latitude, 27.3390, places=4)
        self.assertAlmostEqual(poi.longitude, 88.5938, places=4)

    def test_audio_poi_ordering(self):
        """Test ordering by monastery and order."""
        poi1 = AudioPOI.objects.create(order=2, **self.poi_data)
        poi2_data = self.poi_data.copy()
        poi2_data['title'] = 'Courtyard'
        poi2_data['order'] = 1
        poi2 = AudioPOI.objects.create(**poi2_data)

        pois = AudioPOI.objects.all()
        self.assertEqual(pois[0], poi2)  # Lower order should come first
        self.assertEqual(pois[1], poi1)
