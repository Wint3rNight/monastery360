"""
Django app configuration for the core application.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        """Import signal handlers when the app is ready."""
        # Import any signals here if needed
        pass
