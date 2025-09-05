"""
Django app configuration for the archives application.
"""

from django.apps import AppConfig


class ArchivesConfig(AppConfig):
    """Configuration for the archives app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archives'
    verbose_name = 'Digital Archives'
