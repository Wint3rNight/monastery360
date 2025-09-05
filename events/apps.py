"""
Django app configuration for the events application.
"""

from django.apps import AppConfig


class EventsConfig(AppConfig):
    """Configuration for the events app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    verbose_name = 'Events & Calendar'
