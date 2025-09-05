"""
Tests for archives models and functionality.
"""

from django.test import TestCase

from archives.models import ArchiveItem

# from django.contrib.gis.geos import Point  # Disabled for demo
from core.models import Monastery


class ArchiveItemModelTest(TestCase):
    """Test cases for ArchiveItem model."""

    def setUp(self):
        """Set up test data."""
        self.monastery = Monastery.objects.create(
            name='Test Monastery',
            established_year=1800,
            description='A test monastery.',
            short_description='Test monastery.',
            location=Point(88.5937, 27.3389),
            address='Test Address',
            district='East Sikkim',
            image_alt='Test image',
        )

        self.archive_data = {
            'monastery': self.monastery,
            'title': 'Ancient Manuscript',
            'description': 'A historical manuscript from the 18th century.',
            'item_type': 'manuscript',
            'catalog_number': 'TEST001',
            'material': 'paper',
            'condition': 'good',
            'image_alt': 'Ancient manuscript image',
        }

    def test_archive_item_creation(self):
        """Test archive item creation."""
        item = ArchiveItem.objects.create(**self.archive_data)
        self.assertEqual(item.title, 'Ancient Manuscript')
        self.assertEqual(item.catalog_number, 'TEST001')
        self.assertEqual(item.item_type, 'manuscript')
        self.assertTrue(item.is_public)

    def test_archive_item_str_representation(self):
        """Test string representation."""
        item = ArchiveItem.objects.create(**self.archive_data)
        expected_str = "TEST001: Ancient Manuscript"
        self.assertEqual(str(item), expected_str)

    def test_item_type_display_icon(self):
        """Test item type icon mapping."""
        item = ArchiveItem.objects.create(**self.archive_data)
        self.assertEqual(item.item_type_display_icon, 'fas fa-scroll')

    def test_has_high_res_scan(self):
        """Test has_high_res_scan property."""
        item = ArchiveItem.objects.create(**self.archive_data)
        self.assertFalse(item.has_high_res_scan)  # No scan uploaded

    def test_view_count_increment(self):
        """Test view count increment."""
        item = ArchiveItem.objects.create(**self.archive_data)
        initial_count = item.view_count
        item.increment_view_count()
        item.refresh_from_db()
        self.assertEqual(item.view_count, initial_count + 1)
