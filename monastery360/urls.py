"""
URL configuration for monastery360 project.

This file defines the main URL patterns and includes patterns from individual apps.
It also handles static and media file serving during development.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView


# Simple robots.txt view
def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: {}/sitemap.xml
""".format(request.build_absolute_uri('/'))
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include('api.urls')),

    # Internationalization
    path('i18n/', include('django.conf.urls.i18n')),

    # Apps
    path('', include('core.urls')),
    path('tours/', include('tours.urls')),
    path('archives/', include('archives.urls')),
    path('events/', include('events.urls')),
    path('bookings/', include('bookings.urls')),

    # Authentication is handled by core app
    # All auth URLs are available at: /login/, /logout/, /profile/

    # SEO and PWA
    path('robots.txt', robots_txt, name='robots_txt'),
    path('manifest.webmanifest', TemplateView.as_view(
        template_name='manifest.webmanifest',
        content_type='application/manifest+json'
    ), name='manifest'),
    path('sw.js', TemplateView.as_view(
        template_name='sw.js',
        content_type='application/javascript'
    ), name='service_worker'),
    path('offline/', TemplateView.as_view(
        template_name='offline.html'
    ), name='offline'),
]

# Development-only: serve media and static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Development-only: serve legacy /downloads/ assets referenced by static JSON
    try:
        downloads_root = str(settings.BASE_DIR / 'downloads')
    except Exception:
        # Fallback if BASE_DIR isn't a Path
        downloads_root = os.path.join(settings.BASE_DIR, 'downloads')
    urlpatterns += static('/downloads/', document_root=downloads_root)

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
