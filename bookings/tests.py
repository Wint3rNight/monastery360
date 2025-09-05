"""
Tests for bookings models and functionality.
"""

from datetime import date, timedelta

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking
from core.models import Monastery


class BookingModelTest(TestCase):
    """Test cases for Booking model."""

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

        self.booking_data = {
            'monastery': self.monastery,
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+91-9876543210',
            'visit_date': date.today() + timedelta(days=7),
            'number_of_visitors': 2,
            'number_of_adults': 2,
            'number_of_children': 0,
        }

    def test_booking_creation(self):
        """Test booking creation."""
        booking = Booking.objects.create(**self.booking_data)
        self.assertEqual(booking.name, 'John Doe')
        self.assertEqual(booking.email, 'john@example.com')
        self.assertEqual(booking.status, 'pending')
        self.assertTrue(len(booking.confirmation_number) == 8)

    def test_booking_str_representation(self):
        """Test string representation."""
        booking = Booking.objects.create(**self.booking_data)
        expected_str = f"John Doe - {self.monastery.name} on {booking.visit_date}"
        self.assertEqual(str(booking), expected_str)

    def test_confirmation_number_generation(self):
        """Test automatic confirmation number generation."""
        booking1 = Booking.objects.create(**self.booking_data)
        self.booking_data['email'] = 'jane@example.com'
        booking2 = Booking.objects.create(**self.booking_data)

        self.assertNotEqual(booking1.confirmation_number, booking2.confirmation_number)
        self.assertTrue(len(booking1.confirmation_number) == 8)
        self.assertTrue(len(booking2.confirmation_number) == 8)

    def test_booking_status_upcoming(self):
        """Test upcoming booking status."""
        booking = Booking.objects.create(**self.booking_data)
        self.assertTrue(booking.is_upcoming)
        self.assertFalse(booking.is_past)
        self.assertFalse(booking.is_today)

    def test_booking_status_today(self):
        """Test today's booking status."""
        self.booking_data['visit_date'] = date.today()
        booking = Booking.objects.create(**self.booking_data)
        self.assertTrue(booking.is_today)
        self.assertFalse(booking.is_past)

    def test_booking_status_past(self):
        """Test past booking status."""
        self.booking_data['visit_date'] = date.today() - timedelta(days=1)
        booking = Booking.objects.create(**self.booking_data)
        self.assertTrue(booking.is_past)
        self.assertFalse(booking.is_upcoming)
        self.assertFalse(booking.is_today)

    def test_days_until_visit(self):
        """Test days until visit calculation."""
        booking = Booking.objects.create(**self.booking_data)
        self.assertEqual(booking.days_until_visit, 7)

    def test_needs_confirmation(self):
        """Test needs confirmation status."""
        booking = Booking.objects.create(**self.booking_data)
        self.assertTrue(booking.needs_confirmation)

        booking.status = 'confirmed'
        booking.save()
        self.assertFalse(booking.needs_confirmation)

    def test_visit_type_display_icon(self):
        """Test visit type icon mapping."""
        booking = Booking.objects.create(**self.booking_data)
        self.assertEqual(booking.visit_type_display_icon, 'fas fa-eye')
