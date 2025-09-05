"""
Django app configuration for the tours application.
"""

from django.apps import AppConfig


class ToursConfig(AppConfig):
    """Configuration for the tours app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tours'
    verbose_name = 'Virtual Tours'
