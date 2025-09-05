"""
Core views for Monastery360.

Handles the main website views including homepage, monastery details,
and error pages.
"""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from archives.models import ArchiveItem
from events.models import Event
from tours.models import Panorama

from .models import AudioPOI, Monastery


def home(request):
    """
    React-based homepage with Tailwind CSS styling.
    """
    return render(request, 'core/home_standalone.html')


def monastery_detail(request, slug):
    """
    Detailed view of a monastery including all related content.
    """
    monastery = get_object_or_404(Monastery, slug=slug, is_active=True)

    # Get related content
    audio_pois = monastery.audio_pois.filter(is_active=True).order_by('order')
    panoramas = monastery.panoramas.filter(is_active=True).order_by('order')

    # Upcoming events
    upcoming_events = monastery.events.filter(
        start_time__gte=timezone.now(),
        is_public=True,
        is_cancelled=False
    ).order_by('start_time')[:5]

    # Recent archive items
    archive_items = monastery.archive_items.filter(
        is_public=True
    ).order_by('-created_at')[:6]

    # Archive items by type for quick stats
    archive_stats = monastery.archive_items.filter(
        is_public=True
    ).values('item_type').annotate(
        count=Count('item_type')
    ).order_by('-count')

    context = {
        'monastery': monastery,
        'audio_pois': audio_pois,
        'panoramas': panoramas,
        'upcoming_events': upcoming_events,
        'archive_items': archive_items,
        'archive_stats': archive_stats,
        'page_title': f'{monastery.name} - Monastery360',
        'page_description': monastery.short_description,
        'canonical_url': request.build_absolute_uri(monastery.get_absolute_url()),
    }

    return render(request, 'core/monastery_detail.html', context)


def monastery_list(request):
    """
    List view of all monasteries with search and filtering.
    """
    monasteries = Monastery.objects.filter(is_active=True)

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        monasteries = monasteries.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(district__icontains=search_query)
        )

    # District filtering
    district_filter = request.GET.get('district', '').strip()
    if district_filter:
        monasteries = monasteries.filter(district__iexact=district_filter)

    # Get all districts for filter dropdown
    districts = Monastery.objects.filter(
        is_active=True
    ).values_list('district', flat=True).distinct().order_by('district')

    # Ordering
    order_by = request.GET.get('order', 'name')
    if order_by == 'newest':
        monasteries = monasteries.order_by('-created_at')
    elif order_by == 'oldest':
        monasteries = monasteries.order_by('established_year')
    else:
        monasteries = monasteries.order_by('name')

    # Pagination
    paginator = Paginator(monasteries, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'district_filter': district_filter,
        'districts': districts,
        'order_by': order_by,
        'total_count': monasteries.count(),
        'page_title': 'All Monasteries - Monastery360',
        'page_description': 'Browse all Buddhist monasteries in Sikkim with detailed information, virtual tours, and historical archives.',
    }

    return render(request, 'core/monastery_list.html', context)


def monastery_map(request):
    """
    Interactive map view showing all monasteries with their locations.
    """
    return render(request, 'core/monastery_map.html')


def search(request):
    """
    Global search across monasteries, events, and archive items.
    """
    query = request.GET.get('q', '').strip()
    results = {}

    if query and len(query) >= 2:
        # Search monasteries
        monasteries = Monastery.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(district__icontains=query),
            is_active=True
        )[:5]

        # Search events
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_public=True,
            is_cancelled=False
        ).select_related('monastery')[:5]

        # Search archive items
        archive_items = ArchiveItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cultural_significance__icontains=query),
            is_public=True
        ).select_related('monastery')[:5]

        results = {
            'monasteries': monasteries,
            'events': events,
            'archive_items': archive_items,
            'total_results': len(monasteries) + len(events) + len(archive_items),
        }

    context = {
        'query': query,
        'results': results,
        'page_title': f'Search Results for "{query}"' if query else 'Search - Monastery360',
        'page_description': 'Search monasteries, events, and historical archives across Sikkim.',
    }

    return render(request, 'core/search.html', context)


def custom_404(request, exception):
    """Custom 404 error page."""
    context = {
        'page_title': 'Page Not Found - Monastery360',
        'page_description': 'The page you are looking for does not exist.',
    }
    return render(request, '404.html', context, status=404)


def custom_500(request):
    """Custom 500 error page."""
    context = {
        'page_title': 'Server Error - Monastery360',
        'page_description': 'An internal server error occurred.',
    }
    return render(request, '500.html', context, status=500)


def offline_view(request):
    """Offline page for PWA"""
    context = {
        'page_title': 'Offline - Monastery360',
        'page_description': 'You are currently offline. Some features may not be available.',
    }
    return render(request, 'offline.html', context)
