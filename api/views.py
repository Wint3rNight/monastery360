"""
API views for Monastery360.

Provides REST API endpoints for accessing monastery data, events, and archives.
"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from archives.models import ArchiveItem
from core.models import Monastery
from events.models import Event


class MonasteryListAPIView(generics.ListAPIView):
    """
    API endpoint to list all active monasteries.

    Returns basic information about all monasteries including
    location data for mapping applications.
    """

    def get(self, request):
        monasteries = Monastery.objects.filter(is_active=True).order_by('name')
        data = []

        for monastery in monasteries:
            monastery_data = {
                'id': monastery.id,
                'name': monastery.name,
                'slug': monastery.slug,
                'short_description': monastery.short_description,
                'district': monastery.district,
                'established_year': monastery.established_year,
                'location': {
                    'latitude': monastery.latitude,
                    'longitude': monastery.longitude,
                } if monastery.location else None,
                'address': monastery.address,
                'visiting_hours': monastery.visiting_hours,
                'entry_fee': monastery.entry_fee,
                'image_url': monastery.image.url if monastery.image else None,
                'url': monastery.get_absolute_url(),
                'is_featured': monastery.is_featured,
            }
            data.append(monastery_data)

        return Response({
            'count': len(data),
            'results': data
        })


class MonasteryDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint to get detailed information about a specific monastery.

    Includes related data like audio POIs, panoramas, and recent events.
    """

    def get(self, request, slug):
        monastery = get_object_or_404(Monastery, slug=slug, is_active=True)

        # Get related data
        audio_pois = monastery.audio_pois.filter(is_active=True).order_by('order')
        panoramas = monastery.panoramas.filter(is_active=True).order_by('order')
        upcoming_events = monastery.events.filter(
            start_time__gte=timezone.now(),
            is_public=True,
            is_cancelled=False
        ).order_by('start_time')[:5]

        data = {
            'id': monastery.id,
            'name': monastery.name,
            'slug': monastery.slug,
            'description': monastery.description,
            'short_description': monastery.short_description,
            'established_year': monastery.established_year,
            'district': monastery.district,
            'altitude': monastery.altitude,
            'location': {
                'latitude': monastery.latitude,
                'longitude': monastery.longitude,
            } if monastery.location else None,
            'address': monastery.address,
            'visiting_hours': monastery.visiting_hours,
            'entry_fee': monastery.entry_fee,
            'phone': monastery.phone,
            'email': monastery.email,
            'website': monastery.website,
            'image_url': monastery.image.url if monastery.image else None,
            'image_alt': monastery.image_alt,
            'audio_pois': [
                {
                    'id': poi.id,
                    'title': poi.title,
                    'description': poi.description,
                    'location': {
                        'latitude': poi.latitude,
                        'longitude': poi.longitude,
                    } if poi.location else None,
                    'audio_url': poi.audio_file.url if poi.audio_file else None,
                    'audio_duration': poi.audio_duration,
                    'order': poi.order,
                }
                for poi in audio_pois
            ],
            'panoramas': [
                {
                    'id': panorama.id,
                    'title': panorama.title,
                    'description': panorama.description,
                    'location_name': panorama.location_name,
                    'image_url': panorama.image.url if panorama.image else None,
                    'thumbnail_url': panorama.thumbnail.url if panorama.thumbnail else None,
                    'narration_audio_url': panorama.narration_audio.url if panorama.narration_audio else None,
                    'audio_duration': panorama.audio_duration,
                    'view_count': panorama.view_count,
                    'order': panorama.order,
                    'url': panorama.get_absolute_url(),
                }
                for panorama in panoramas
            ],
            'upcoming_events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'short_description': event.short_description,
                    'event_type': event.event_type,
                    'start_time': event.start_time.isoformat(),
                    'end_time': event.end_time.isoformat(),
                    'location_details': event.location_details,
                    'entry_fee': event.entry_fee,
                    'url': event.get_absolute_url(),
                }
                for event in upcoming_events
            ],
            'statistics': {
                'total_panoramas': panoramas.count(),
                'total_audio_pois': audio_pois.count(),
                'total_archive_items': monastery.archive_items.filter(is_public=True).count(),
                'upcoming_events_count': upcoming_events.count(),
            }
        }

        return Response(data)


class EventListAPIView(generics.ListAPIView):
    """
    API endpoint to list upcoming public events.

    Returns events from all monasteries that are public and not cancelled.
    """

    def get(self, request):
        events = Event.objects.filter(
            start_time__gte=timezone.now(),
            is_public=True,
            is_cancelled=False
        ).select_related('monastery').order_by('start_time')

        # Optional filtering by monastery
        monastery_slug = request.GET.get('monastery')
        if monastery_slug:
            events = events.filter(monastery__slug=monastery_slug)

        # Optional filtering by event type
        event_type = request.GET.get('type')
        if event_type:
            events = events.filter(event_type=event_type)

        # Limit results
        limit = min(int(request.GET.get('limit', 20)), 100)
        events = events[:limit]

        data = []
        for event in events:
            event_data = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'short_description': event.short_description,
                'event_type': event.event_type,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat(),
                'is_all_day': event.is_all_day,
                'location_details': event.location_details,
                'entry_fee': event.entry_fee,
                'requires_registration': event.requires_registration,
                'max_participants': event.max_participants,
                'language': event.language,
                'dress_code': event.dress_code,
                'image_url': event.image.url if event.image else None,
                'monastery': {
                    'id': event.monastery.id,
                    'name': event.monastery.name,
                    'slug': event.monastery.slug,
                    'district': event.monastery.district,
                },
                'url': event.get_absolute_url(),
                'status': event.status,
                'duration_hours': event.duration_hours,
            }
            data.append(event_data)

        return Response({
            'count': len(data),
            'results': data
        })


class ArchiveListAPIView(generics.ListAPIView):
    """
    API endpoint to list archive items for a specific monastery.

    Returns digital archive items that are marked as public.
    """

    def get(self, request, monastery_slug):
        monastery = get_object_or_404(Monastery, slug=monastery_slug, is_active=True)
        archive_items = ArchiveItem.objects.filter(
            monastery=monastery,
            is_public=True
        ).order_by('catalog_number')

        # Optional filtering by item type
        item_type = request.GET.get('type')
        if item_type:
            archive_items = archive_items.filter(item_type=item_type)

        # Optional filtering by material
        material = request.GET.get('material')
        if material:
            archive_items = archive_items.filter(material=material)

        # Limit results
        limit = min(int(request.GET.get('limit', 20)), 100)
        archive_items = archive_items[:limit]

        data = []
        for item in archive_items:
            item_data = {
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'item_type': item.item_type,
                'catalog_number': item.catalog_number,
                'material': item.material,
                'condition': item.condition,
                'estimated_age': item.estimated_age,
                'historical_period': item.historical_period,
                'cultural_significance': item.cultural_significance,
                'dimensions': item.dimensions,
                'language': item.language,
                'script': item.script,
                'image_url': item.image.url if item.image else None,
                'image_alt': item.image_alt,
                'scan_url': item.scan.url if item.scan else None,
                'scan_resolution': item.scan_resolution,
                'has_high_res_scan': item.has_high_res_scan,
                'item_type_icon': item.item_type_display_icon,
                'view_count': item.view_count,
                'url': item.get_absolute_url(),
            }
            data.append(item_data)

        return Response({
            'monastery': {
                'id': monastery.id,
                'name': monastery.name,
                'slug': monastery.slug,
            },
            'count': len(data),
            'results': data
        })


@api_view(['GET'])
def api_overview(request):
    """
    API overview endpoint listing all available endpoints.
    """
    endpoints = {
        'overview': '/api/',
        'monasteries': '/api/monasteries/',
        'monastery_detail': '/api/monasteries/<slug>/',
        'events': '/api/events/',
        'archives': '/api/archives/<monastery_slug>/',
    }

    return Response({
        'message': 'Welcome to the Monastery360 API',
        'version': '1.0',
        'endpoints': endpoints,
        'documentation': 'Visit the individual endpoints for detailed information'
    })
