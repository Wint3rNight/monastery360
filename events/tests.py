"""
Tests for events models and functionality.
"""

from datetime import timedelta

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils import timezone

from core.models import Monastery
from events.models import Event


class EventModelTest(TestCase):
    """Test cases for Event model."""

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

        now = timezone.now()
        self.event_data = {
            'monastery': self.monastery,
            'title': 'Test Festival',
            'description': 'A test festival event.',
            'short_description': 'Test festival.',
            'event_type': 'festival',
            'start_time': now + timedelta(days=7),
            'end_time': now + timedelta(days=7, hours=6),
        }

    def test_event_creation(self):
        """Test event creation."""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.title, 'Test Festival')
        self.assertEqual(event.event_type, 'festival')
        self.assertTrue(event.is_public)
        self.assertFalse(event.is_featured)

    def test_event_str_representation(self):
        """Test string representation."""
        event = Event.objects.create(**self.event_data)
        expected_str = f"Test Festival - {event.start_time.strftime('%Y-%m-%d')}"
        self.assertEqual(str(event), expected_str)

    def test_event_status_upcoming(self):
        """Test upcoming event status."""
        event = Event.objects.create(**self.event_data)
        self.assertTrue(event.is_upcoming)
        self.assertFalse(event.is_ongoing)
        self.assertFalse(event.is_past)
        self.assertEqual(event.status, 'upcoming')

    def test_event_status_ongoing(self):
        """Test ongoing event status."""
        now = timezone.now()
        self.event_data['start_time'] = now - timedelta(hours=1)
        self.event_data['end_time'] = now + timedelta(hours=1)
        event = Event.objects.create(**self.event_data)

        self.assertFalse(event.is_upcoming)
        self.assertTrue(event.is_ongoing)
        self.assertFalse(event.is_past)
        self.assertEqual(event.status, 'ongoing')

    def test_event_status_past(self):
        """Test past event status."""
        now = timezone.now()
        self.event_data['start_time'] = now - timedelta(days=2)
        self.event_data['end_time'] = now - timedelta(days=1)
        event = Event.objects.create(**self.event_data)

        self.assertFalse(event.is_upcoming)
        self.assertFalse(event.is_ongoing)
        self.assertTrue(event.is_past)
        self.assertEqual(event.status, 'completed')

    def test_event_duration_hours(self):
        """Test duration calculation."""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.duration_hours, 6.0)

    def test_registration_open(self):
        """Test registration status."""
        self.event_data['requires_registration'] = True
        self.event_data['registration_deadline'] = timezone.now() + timedelta(days=3)
        event = Event.objects.create(**self.event_data)
        self.assertTrue(event.registration_open)
