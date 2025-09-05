"""
Django app configuration for the bookings application.
"""

from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """Configuration for the bookings app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'
    verbose_name = 'Visitor Bookings'
