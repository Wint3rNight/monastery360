"""
Django admin configuration for core models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import AudioPOI, Monastery
from .models import ContactSubmission, Feedback


@admin.register(Monastery)
class MonasteryAdmin(admin.ModelAdmin):
    """Admin configuration for Monastery model."""

    list_display = [
        'name', 'district', 'established_year',
        'is_active', 'is_featured', 'created_at'
    ]
    list_filter = [
        'district', 'is_active', 'is_featured',
        'established_year', 'created_at'
    ]
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'slug', 'established_year',
                'description', 'short_description'
            )
        }),
        ('Location', {
            'fields': (
                'location', 'address', 'district', 'altitude'
            )
        }),
        ('Media', {
            'fields': (
                'image', 'image_alt'
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone', 'email', 'website'
            )
        }),
        ('Visitor Information', {
            'fields': (
                'visiting_hours', 'entry_fee'
            )
        }),
        ('Settings', {
            'fields': (
                'is_active', 'is_featured'
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(AudioPOI)
class AudioPOIAdmin(admin.ModelAdmin):
    """Admin configuration for AudioPOI model."""

    list_display = [
        'title', 'monastery', 'audio_duration',
        'order', 'is_active', 'created_at'
    ]
    list_filter = [
        'monastery', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'monastery__name']
    autocomplete_fields = ['monastery']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'monastery', 'title', 'description', 'order'
            )
        }),
        ('Location', {
            'fields': (
                'location',
            )
        }),
        ('Audio Content', {
            'fields': (
                'audio_file', 'audio_duration', 'audio_transcript'
            )
        }),
        ('Settings', {
            'fields': (
                'is_active',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )


# Unregister the default User admin and register our custom one
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User admin with additional display options."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin for contact form submissions."""
    
    list_display = ('name', 'email', 'subject', 'created_at', 'is_responded')
    list_filter = ('subject', 'is_responded', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Admin Response', {
            'fields': ('is_responded', 'response_date', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('user', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin for user feedback."""
    
    list_display = ('name', 'category', 'rating', 'title', 'created_at', 'is_reviewed')
    list_filter = ('category', 'rating', 'is_reviewed', 'is_public', 'created_at')
    search_fields = ('name', 'email', 'title', 'message')
    readonly_fields = ('created_at', 'browser_info')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'user')
        }),
        ('Feedback Content', {
            'fields': ('category', 'rating', 'title', 'message')
        }),
        ('Additional Info', {
            'fields': ('page_url', 'browser_info'),
            'classes': ('collapse',)
        }),
        ('Admin Actions', {
            'fields': ('is_reviewed', 'is_public', 'admin_response'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

