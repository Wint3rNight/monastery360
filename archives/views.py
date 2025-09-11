"""
Archives views for Monastery360.

Handles digital archives portal and API endpoints.
"""

import json
import os

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from core.models import Monastery

from .models import ArchiveItem


def item_detail(request, monastery_slug, catalog_number):
    """Render a single archive item detail page."""
    item = ArchiveItem.objects.select_related('monastery').filter(
        monastery__slug=monastery_slug,
        catalog_number=catalog_number,
        is_public=True
    ).first()

    if not item:
        from django.http import Http404
        raise Http404('Archive item not found')

    context = {
        'item': item,
        'page_title': f'{item.title} - {item.monastery.name}',
        'page_description': item.description[:160],
    }

    return render(request, 'archives/item_detail.html', context)


def item_download(request, monastery_slug, catalog_number):
    """Serve the archive scan file and increment download counter.

    If `?inline=1` is provided, attempt to display inline (Content-Disposition inline).
    Otherwise serve as attachment.
    """
    import mimetypes

    from django.http import FileResponse, Http404, HttpResponse

    item = ArchiveItem.objects.select_related('monastery').filter(
        monastery__slug=monastery_slug,
        catalog_number=catalog_number,
        is_public=True
    ).first()

    if not item or not item.scan:
        raise Http404('File not found')

    # Check if file exists
    try:
        if not item.scan.storage.exists(item.scan.name):
            raise Http404('File not found on storage')
    except Exception:
        raise Http404('File not accessible')

    # increment download counter (best-effort)
    try:
        item.increment_download_count()
    except Exception:
        pass

    # Determine disposition and content type
    inline = request.GET.get('inline') == '1'
    disposition = 'inline' if inline else 'attachment'

    # Get file name
    filename = os.path.basename(item.scan.name)

    # Determine content type
    content_type, _ = mimetypes.guess_type(filename)
    if not content_type:
        content_type = 'application/octet-stream'

    try:
        # Use FileResponse for better performance
        response = FileResponse(
            item.scan.open('rb'),
            as_attachment=(not inline),
            content_type=content_type
        )
        response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
        return response
    except Exception as e:
        # Fallback: return error message
        return HttpResponse(f'Error serving file: {str(e)}', status=500)


def archive_index(request):
    """
    Main archives page with featured items and statistics.
    """
    # Featured archive items
    featured_items = ArchiveItem.objects.filter(
        is_public=True
    ).select_related('monastery').order_by('-view_count')[:6]

    # Statistics by item type
    item_type_stats = ArchiveItem.objects.filter(
        is_public=True
    ).values('item_type').annotate(
        count=Count('item_type')
    ).order_by('-count')

    # Statistics by monastery
    monastery_stats = ArchiveItem.objects.filter(
        is_public=True
    ).values(
        'monastery__name', 'monastery__slug'
    ).annotate(
        count=Count('monastery')
    ).order_by('-count')[:5]

    # Recent additions
    recent_items = ArchiveItem.objects.filter(
        is_public=True
    ).select_related('monastery').order_by('-created_at')[:4]

    total_items = ArchiveItem.objects.filter(is_public=True).count()
    total_monasteries = Monastery.objects.filter(
        is_active=True,
        archive_items__is_public=True
    ).distinct().count()

    context = {
        'featured_items': featured_items,
        'item_type_stats': item_type_stats,
        'monastery_stats': monastery_stats,
        'recent_items': recent_items,
        'total_items': total_items,
        'total_monasteries': total_monasteries,
        'page_title': 'Digital Archives Portal - Sikkim Monasteries',
        'page_description': 'Explore our comprehensive collection of digitally preserved manuscripts, artworks, and historical documents from Sikkim\'s monasteries.',
    }

    return render(request, 'archives/index.html', context)


def digital_portal(request):
    """
    New digital archives portal with clean React implementation.
    """
    return render(request, 'archives/digital_portal.html')


def archives_api(request):
    """
    API endpoint to fetch archives data from JSON file.
    """
    try:
        json_path = os.path.join(settings.STATIC_ROOT or 'static', 'data', 'archives.json')
        if not os.path.exists(json_path):
            json_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'archives.json')

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
