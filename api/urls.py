"""
URL configuration for API endpoints.
"""

from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    # API overview
    path('', views.api_overview, name='overview'),

    # Monasteries
    path('monasteries/', views.MonasteryListAPIView.as_view(), name='monastery_list'),
    path('monasteries/<slug:slug>/', views.MonasteryDetailAPIView.as_view(), name='monastery_detail'),

    # Events
    path('events/', views.EventListAPIView.as_view(), name='event_list'),

    # Archives
    path('archives/<slug:monastery_slug>/', views.ArchiveListAPIView.as_view(), name='archive_list'),
]
