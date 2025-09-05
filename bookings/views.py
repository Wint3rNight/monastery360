"""
Bookings views for Monastery360.

Handles visitor booking creation, confirmation, and management.
"""

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone

from core.models import Monastery

from .forms import BookingForm, BookingSearchForm
from .models import Booking


def booking_form(request, monastery_slug=None):
    """
    Booking form view for creating new visitor bookings.
    """
    monastery = None
    if monastery_slug:
        monastery = get_object_or_404(Monastery, slug=monastery_slug, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Send confirmation email
            try:
                send_booking_confirmation_email(booking)
                messages.success(
                    request,
                    f'Your booking request has been submitted successfully! '
                    f'Confirmation number: {booking.confirmation_number}. '
                    f'We will contact you within 24-48 hours to confirm your visit.'
                )
            except Exception as e:
                messages.warning(
                    request,
                    f'Your booking was created (#{booking.confirmation_number}) but we could not send the confirmation email. '
                    f'Please note your confirmation number for future reference.'
                )

            return redirect('bookings:thanks', confirmation_number=booking.confirmation_number)
    else:
        # Pre-populate monastery if specified
        initial_data = {}
        if monastery:
            initial_data['monastery'] = monastery
        form = BookingForm(initial=initial_data)

    context = {
        'form': form,
        'monastery': monastery,
        'page_title': f'Book a Visit - {monastery.name}' if monastery else 'Book a Visit - Monastery360',
        'page_description': f'Schedule your visit to {monastery.name}' if monastery else 'Schedule your visit to any monastery in Sikkim',
    }

    return render(request, 'bookings/form.html', context)


def booking_thanks(request, confirmation_number):
    """
    Thank you page after successful booking submission.
    """
    booking = get_object_or_404(Booking, confirmation_number=confirmation_number)

    context = {
        'booking': booking,
        'page_title': 'Booking Confirmed - Monastery360',
        'page_description': 'Your booking request has been submitted successfully.',
    }

    return render(request, 'bookings/thanks.html', context)


def booking_detail(request, confirmation_number):
    """
    View booking details using confirmation number.
    """
    booking = get_object_or_404(Booking, confirmation_number=confirmation_number)

    context = {
        'booking': booking,
        'page_title': f'Booking Details - {booking.confirmation_number}',
        'page_description': f'Booking details for {booking.name} at {booking.monastery.name}',
    }

    return render(request, 'bookings/detail.html', context)


def booking_search(request):
    """
    Search for bookings using confirmation number, email, or phone.
    """
    form = BookingSearchForm(request.GET or None)
    booking = None

    if form.is_valid():
        confirmation_number = form.cleaned_data.get('confirmation_number')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')

        # Search by confirmation number (most specific)
        if confirmation_number:
            try:
                booking = Booking.objects.get(confirmation_number=confirmation_number.upper())
            except Booking.DoesNotExist:
                messages.error(request, f'No booking found with confirmation number: {confirmation_number}')

        # Search by email
        elif email:
            bookings = Booking.objects.filter(email__iexact=email).order_by('-created_at')
            if bookings.exists():
                booking = bookings.first()
                if bookings.count() > 1:
                    messages.info(
                        request,
                        f'Multiple bookings found for this email. Showing the most recent one. '
                        f'Total bookings: {bookings.count()}'
                    )
            else:
                messages.error(request, f'No booking found with email: {email}')

        # Search by phone
        elif phone:
            bookings = Booking.objects.filter(phone__icontains=phone).order_by('-created_at')
            if bookings.exists():
                booking = bookings.first()
                if bookings.count() > 1:
                    messages.info(
                        request,
                        f'Multiple bookings found for this phone number. Showing the most recent one. '
                        f'Total bookings: {bookings.count()}'
                    )
            else:
                messages.error(request, f'No booking found with phone number: {phone}')

    context = {
        'form': form,
        'booking': booking,
        'page_title': 'Find Your Booking - Monastery360',
        'page_description': 'Search for your booking using confirmation number, email, or phone number.',
    }

    return render(request, 'bookings/search.html', context)


def send_booking_confirmation_email(booking):
    """
    Send confirmation email to the visitor.
    """
    subject = f'Booking Confirmation - {booking.monastery.name} Visit'

    # Render email content
    email_content = render_to_string('bookings/emails/confirmation.html', {
        'booking': booking,
        'monastery': booking.monastery,
    })

    # Send email
    send_mail(
        subject=subject,
        message='',  # Plain text version (optional)
        html_message=email_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email],
        fail_silently=False,
    )

    # Also send notification to monastery (if email available)
    if booking.monastery.email:
        try:
            monastery_subject = f'New Booking Request - {booking.confirmation_number}'
            monastery_content = render_to_string('bookings/emails/monastery_notification.html', {
                'booking': booking,
                'monastery': booking.monastery,
            })

            send_mail(
                subject=monastery_subject,
                message='',
                html_message=monastery_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.monastery.email],
                fail_silently=True,  # Don't fail if monastery email fails
            )
        except Exception:
            pass  # Silently ignore monastery email failures
