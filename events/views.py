"""
Events views for Monastery360.

Handles event listings, calendar views, and event details.
"""

from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from core.models import Monastery

from .models import Event


def event_calendar(request):
    """
    Cultural Calendar - main events page.
    """
    return render(request, 'events/cultural_calendar.html')


def event_list(request):
    """
    List view of all upcoming events.
    """
    events = Event.objects.filter(
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).select_related('monastery').order_by('start_time')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(monastery__name__icontains=search_query)
        )

    # Filter by monastery
    monastery_slug = request.GET.get('monastery')
    if monastery_slug:
        events = events.filter(monastery__slug=monastery_slug)

    # Filter by event type
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)

    # Filter by time range
    time_range = request.GET.get('time', 'all')
    now = timezone.now()
    if time_range == 'week':
        events = events.filter(start_time__lte=now + timedelta(days=7))
    elif time_range == 'month':
        events = events.filter(start_time__lte=now + timedelta(days=30))
    elif time_range == 'quarter':
        events = events.filter(start_time__lte=now + timedelta(days=90))

    # Get filter options
    monasteries = Monastery.objects.filter(
        is_active=True,
        events__is_public=True,
        events__is_cancelled=False,
        events__start_time__gte=timezone.now()
    ).distinct().order_by('name')

    event_types = Event.objects.filter(
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).values_list('event_type', flat=True).distinct()

    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'monasteries': monasteries,
        'event_types': event_types,
        'selected_monastery': monastery_slug,
        'selected_type': event_type,
        'selected_time': time_range,
        'total_count': events.count(),
        'page_title': 'Upcoming Events - Monastery360',
        'page_description': 'Discover upcoming festivals, ceremonies, and events at Buddhist monasteries in Sikkim.',
    }

    return render(request, 'events/list.html', context)


def event_by_monastery(request, slug):
    """
    Events filtered by a specific monastery.
    """
    monastery = get_object_or_404(Monastery, slug=slug, is_active=True)

    events = Event.objects.filter(
        monastery=monastery,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).order_by('start_time')

    # Filter by event type
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)

    # Get available event types for this monastery
    available_types = Event.objects.filter(
        monastery=monastery,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).values_list('event_type', flat=True).distinct()

    # Recent past events for context
    past_events = Event.objects.filter(
        monastery=monastery,
        end_time__lt=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).order_by('-start_time')[:3]

    # Pagination
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'monastery': monastery,
        'page_obj': page_obj,
        'available_types': available_types,
        'selected_type': event_type,
        'past_events': past_events,
        'total_upcoming': events.count(),
        'page_title': f'{monastery.name} Events - Monastery360',
        'page_description': f'Upcoming festivals, ceremonies, and events at {monastery.name}.',
        'canonical_url': request.build_absolute_uri(),
    }

    return render(request, 'events/by_monastery.html', context)


def event_detail(request, monastery_slug, event_id):
    """
    Detailed view of a specific event.
    """
    monastery = get_object_or_404(Monastery, slug=monastery_slug, is_active=True)
    event = get_object_or_404(
        Event,
        id=event_id,
        monastery=monastery,
        is_public=True
    )

    # Get related events from the same monastery
    related_events = Event.objects.filter(
        monastery=monastery,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).exclude(id=event.id).order_by('start_time')[:3]

    # Get similar events by type
    similar_events = Event.objects.filter(
        event_type=event.event_type,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).exclude(id=event.id).select_related('monastery').order_by('start_time')[:3]

    context = {
        'monastery': monastery,
        'event': event,
        'related_events': related_events,
        'similar_events': similar_events,
        'page_title': f'{event.title} - {monastery.name}',
        'page_description': event.short_description,
        'canonical_url': request.build_absolute_uri(event.get_absolute_url()),
    }

    return render(request, 'events/detail.html', context)


def get_event_color(event_type):
    """
    Return a color code for different event types for calendar display.
    """
    colors = {
        'festival': '#ff6b6b',      # Red
        'ceremony': '#4ecdc4',      # Teal
        'teaching': '#45b7d1',      # Blue
        'meditation': '#96ceb4',    # Green
        'celebration': '#feca57',   # Yellow
        'pilgrimage': '#ff9ff3',    # Pink
        'cultural': '#54a0ff',      # Light Blue
        'educational': '#5f27cd',   # Purple
        'maintenance': '#999999',   # Gray
        'other': '#c8d6e5',        # Light Gray
    }
    return colors.get(event_type, '#c8d6e5')


def full_calendar_view(request):
    """
    Full calendar view showing all events in a list format.
    """
    # Get all events (past and future) for React to handle filtering
    events = Event.objects.filter(
        is_public=True,
        is_cancelled=False
    ).select_related('monastery').order_by('start_time')

    # Don't apply server-side filtering - let React handle it all
    # This ensures the search and filter functions work properly

    context = {
        'events': events,  # Pass all events for React to handle
        'event_types': Event.EVENT_TYPES,
        'page_title': 'Full Calendar - All Events',
    }

    return render(request, 'events/full_calendar_enhanced.html', context)


def event_detail_simple(request, event_id):
    """
    Simple event detail view without monastery slug.
    """
    event = get_object_or_404(Event, id=event_id, is_public=True)
    monastery = event.monastery

    # Get related events from the same monastery
    related_events = Event.objects.filter(
        monastery=monastery,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).exclude(id=event.id).select_related('monastery').order_by('start_time')[:3]

    # Get similar events (same type)
    similar_events = Event.objects.filter(
        event_type=event.event_type,
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).exclude(id=event.id).select_related('monastery').order_by('start_time')[:3]

    context = {
        'monastery': monastery,
        'event': event,
        'related_events': related_events,
        'similar_events': similar_events,
        'page_title': f'{event.title} - {monastery.name}',
        'page_description': event.short_description,
        'canonical_url': request.build_absolute_uri(event.get_absolute_url()),
    }

    return render(request, 'events/detail_enhanced.html', context)
