"""
URL configuration for events app.
"""

from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    # Events main pages
    path('', views.event_calendar, name='calendar'),
    path('list/', views.event_list, name='list'),

    # Monastery-specific events
    path('monastery/<slug:slug>/', views.event_by_monastery, name='by_monastery'),

    # Individual events
    path('event/<slug:monastery_slug>/<int:event_id>/', views.event_detail, name='event_detail'),
]
