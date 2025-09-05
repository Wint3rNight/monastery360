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

    # Booking management
    path('thanks/<str:confirmation_number>/', views.booking_thanks, name='thanks'),
    path('search/', views.booking_search, name='search'),
    path('booking/<str:confirmation_number>/', views.booking_detail, name='booking_detail'),
]
