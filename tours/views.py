"""
Tours views for Monastery360.

Handles virtual tour functionality including panorama viewing
and interactive tour experiences.
"""

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.models import Monastery

from .models import Panorama


def virtual_tours_gallery(request):
    """
    Virtual tours gallery page with React frontend.
    """
    return render(request, 'tours/virtual_tours.html')


def panorama_list(request):
    """
    List view of all available panoramas across monasteries.
    """
    panoramas = Panorama.objects.filter(
        is_active=True,
        monastery__is_active=True
    ).select_related('monastery').order_by('monastery__name', 'order')

    # Filter by monastery if specified
    monastery_slug = request.GET.get('monastery')
    if monastery_slug:
        panoramas = panoramas.filter(monastery__slug=monastery_slug)

    # Get monasteries for filter dropdown
    monasteries = Monastery.objects.filter(
        is_active=True,
        panoramas__is_active=True
    ).distinct().order_by('name')

    # Pagination
    paginator = Paginator(panoramas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'monasteries': monasteries,
        'selected_monastery': monastery_slug,
        'total_count': panoramas.count(),
        'page_title': 'Virtual Tours - Monastery360',
        'page_description': 'Take immersive 360-degree virtual tours of Buddhist monasteries in Sikkim.',
    }

    return render(request, 'tours/panorama_list.html', context)


def panorama_detail(request, monastery_slug, panorama_id):
    """
    Detailed view for a specific panorama with interactive viewer.
    """
    monastery = get_object_or_404(Monastery, slug=monastery_slug, is_active=True)
    panorama = get_object_or_404(
        Panorama,
        id=panorama_id,
        monastery=monastery,
        is_active=True
    )

    # Increment view count
    panorama.increment_view_count()

    # Get other panoramas from the same monastery
    other_panoramas = Panorama.objects.filter(
        monastery=monastery,
        is_active=True
    ).exclude(id=panorama.id).order_by('order')

    # Get related content
    audio_pois = monastery.audio_pois.filter(is_active=True).order_by('order')
    archive_items = monastery.archive_items.filter(is_public=True)[:3]

    context = {
        'monastery': monastery,
        'panorama': panorama,
        'other_panoramas': other_panoramas,
        'audio_pois': audio_pois,
        'archive_items': archive_items,
        'page_title': f'{panorama.title} - {monastery.name}',
        'page_description': panorama.description,
        'canonical_url': request.build_absolute_uri(panorama.get_absolute_url()),
    }

    return render(request, 'tours/panorama_detail.html', context)


def monastery_tour(request, slug):
    """
    Complete virtual tour experience for a monastery.
    """
    monastery = get_object_or_404(Monastery, slug=slug, is_active=True)

    # Get all panoramas for this monastery
    panoramas = monastery.panoramas.filter(is_active=True).order_by('order')

    if not panoramas.exists():
        # Redirect to monastery detail if no panoramas available
        from django.shortcuts import redirect
        return redirect('core:monastery_detail', slug=slug)

    # Get audio POIs
    audio_pois = monastery.audio_pois.filter(is_active=True).order_by('order')

    # Prepare data for JavaScript tour navigation
    panorama_data = []
    for panorama in panoramas:
        panorama_data.append({
            'id': panorama.id,
            'title': panorama.title,
            'description': panorama.description,
            'location_name': panorama.location_name,
            'image_url': panorama.image.url if panorama.image else None,
            'narration_audio_url': panorama.narration_audio.url if panorama.narration_audio else None,
            'audio_duration': panorama.audio_duration,
            'audio_transcript': panorama.audio_transcript,
            'initial_yaw': panorama.initial_yaw,
            'initial_pitch': panorama.initial_pitch,
            'hotspots_data': panorama.hotspots_data,
            'order': panorama.order,
        })

    # Prepare audio POI data - guard against POIs without coordinates
    poi_data = []
    for poi in audio_pois:
        # AudioPOI model uses latitude/longitude fields (no 'location' attribute)
        if getattr(poi, 'latitude', None) is not None and getattr(poi, 'longitude', None) is not None:
            poi_data.append({
                'id': poi.id,
                'title': poi.title,
                'description': poi.description,
                'latitude': poi.latitude,
                'longitude': poi.longitude,
                'audio_url': poi.audio_file.url if poi.audio_file else None,
                'audio_duration': poi.audio_duration,
                'audio_transcript': poi.audio_transcript,
                'order': poi.order,
            })

    context = {
        'monastery': monastery,
        'panoramas': panoramas,
        'audio_pois': audio_pois,
        'panorama_data_json': panorama_data,
        'poi_data_json': poi_data,
        # include a small serialized list of archive items for the monastery tour page
        'archive_items': [],
    }

    # build archive items with safe URL and image fallbacks
    archive_qs = monastery.archive_items.filter(is_public=True)[:6]
    archive_list = []
    for a in archive_qs:
        # safe detail url
        try:
            detail = a.get_absolute_url()
        except Exception:
            try:
                detail = reverse('archives:item_detail', kwargs={'monastery_slug': monastery.slug, 'catalog_number': a.catalog_number})
            except Exception:
                detail = f"/archives/portal/?item={a.catalog_number}"

        image_url = None
        try:
            image_url = a.image.url if a.image else None
        except Exception:
            image_url = None

        archive_list.append({
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'image_url': image_url,
            'catalog_number': a.catalog_number,
            'item_type': a.item_type,
            'detail_url': detail,
        })

    context['archive_items'] = archive_list
    # add a few remaining context values
    context.update({
        'first_panorama': panoramas.first(),
        'page_title': f'Virtual Tour - {monastery.name}',
        'page_description': f'Take an immersive virtual tour of {monastery.name} with 360-degree panoramas and audio guides.',
        'canonical_url': request.build_absolute_uri(),
    })

    return render(request, 'tours/monastery_tour.html', context)


def tour_map(request):
    """
    Interactive map showing monasteries with available virtual tours.
    """
    monasteries = Monastery.objects.filter(
        is_active=True,
        panoramas__is_active=True
    ).distinct().order_by('name')

    # Prepare data for map
    monastery_data = []
    for monastery in monasteries:
        panorama_count = monastery.panoramas.filter(is_active=True).count()
        if monastery.location and panorama_count > 0:
            monastery_data.append({
                'id': monastery.id,
                'name': monastery.name,
                'slug': monastery.slug,
                'short_description': monastery.short_description,
                'district': monastery.district,
                'latitude': monastery.latitude,
                'longitude': monastery.longitude,
                'panorama_count': panorama_count,
                'tour_url': f'/tours/monastery/{monastery.slug}/',
                'image_url': monastery.image.url if monastery.image else None,
            })

    context = {
        'monasteries': monasteries,
        'monastery_data_json': monastery_data,
        'total_monasteries': len(monastery_data),
        'page_title': 'Virtual Tour Map - Monastery360',
        'page_description': 'Interactive map showing monasteries with available virtual tours in Sikkim.',
    }

    return render(request, 'tours/tour_map.html', context)


def test_view(request):
    """Simple test view to verify URL routing is working"""
    from django.http import HttpResponse
    return HttpResponse("Test view is working! URL routing is fine.")


def monastery_detail_by_pano(request, pano_id):
    """
    Monastery detail page accessed by pano_id.
    Serves our new monastery_detail.html template.
    """
    import json
    import os

    from django.conf import settings
    from django.http import HttpResponse

    # Debug: Let's first check if the view is being called
    print(f"DEBUG: monastery_detail_by_pano called with pano_id: {pano_id}")

    # Load monastery data from JSON file
    json_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'monasteries.json')
    print(f"DEBUG: Looking for JSON file at: {json_path}")

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        print(f"DEBUG: Loaded JSON data with {len(data.get('monasteries', []))} monasteries")

        # Find monastery by pano_id
        monastery = None
        for m in data['monasteries']:
            if m['panoId'] == pano_id:
                monastery = m
                break

        if not monastery:
            print(f"DEBUG: No monastery found with pano_id: {pano_id}")
            available_pano_ids = [m['panoId'] for m in data['monasteries']]
            print(f"DEBUG: Available pano_ids: {available_pano_ids}")
            from django.http import Http404
            raise Http404(f"Monastery not found. Available IDs: {available_pano_ids}")

        print(f"DEBUG: Found monastery: {monastery['name']}")

        context = {
            'monastery': monastery,
            'page_title': f'{monastery["name"]} - Virtual Tour',
            'page_description': monastery['description'],
        }

        return render(request, 'tours/monastery_detail.html', context)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"DEBUG: Exception occurred: {e}")
        from django.http import Http404
        raise Http404(f"Monastery data not available: {e}")
