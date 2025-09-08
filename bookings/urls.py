"""
URL configuration for bookings app.
"""

from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking creation
    path('', views.booking_form, name='form'),
    path('monastery/<slug:monastery_slug>/', views.booking_form, name='monastery_form'),

    # Event booking
    path('event/<int:event_id>/', views.event_booking_form, name='event_booking'),
    path('event/thanks/<str:confirmation_number>/', views.event_booking_thanks, name='event_booking_thanks'),
    path('event/<str:confirmation_number>/', views.event_booking_detail, name='event_booking_detail'),
    path('event/<str:confirmation_number>/receipt/', views.download_receipt, name='download_receipt'),
    path('event/<str:confirmation_number>/cancel/', views.cancel_event_booking, name='cancel_event_booking'),

    # Regular booking management
    path('thanks/<str:confirmation_number>/', views.booking_thanks, name='thanks'),
    path('search/', views.booking_search, name='search'),
    path('booking/<str:confirmation_number>/', views.booking_detail, name='booking_detail'),
]
