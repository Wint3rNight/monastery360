"""
URL configuration for archives app.
"""

from django.urls import path

from . import views

app_name = 'archives'

urlpatterns = [
    # Archives main pages
    path('', views.archive_index, name='index'),
    path('portal/', views.digital_portal, name='digital_portal'),

    # API endpoints
    path('api/archives/', views.archives_api, name='archives_api'),
    # Item detail (by monastery slug and catalog number)
    path('<slug:monastery_slug>/item/<str:catalog_number>/', views.item_detail, name='item_detail'),
    # download endpoint for archive scans
    path('<slug:monastery_slug>/item/<str:catalog_number>/download/', views.item_download, name='item_download'),
]
