"""
Bookings views for Monastery360.

Handles visitor booking creation, confirmation, and management.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from core.models import Monastery
from events.models import Event

from .forms import BookingForm, BookingSearchForm
from .models import Booking, EventBooking


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
            booking = form.save(commit=False)
            
            # SECURITY FIX: Always link booking to logged-in user if authenticated
            if request.user.is_authenticated:
                booking.user = request.user
                # For logged-in users, use their profile info as default
                if not booking.email or booking.email != request.user.email:
                    booking.email = request.user.email
                if not booking.name and (request.user.first_name or request.user.last_name):
                    booking.name = f"{request.user.first_name} {request.user.last_name}".strip()
                    if not booking.name:  # If no first/last name, use username
                        booking.name = request.user.username
            
            booking.save()

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


@login_required
def event_booking_form(request, event_id):
    """
    Event booking form for cultural calendar events.
    """
    event = get_object_or_404(Event, id=event_id, is_public=True)

    if request.method == 'POST':
        # Get form data
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        number_of_people = int(request.POST.get('number_of_people', 1))
        number_of_adults = int(request.POST.get('number_of_adults', 1))
        number_of_children = int(request.POST.get('number_of_children', 0))
        special_requirements = request.POST.get('special_requirements', '')
        accessibility_needs = request.POST.get('accessibility_needs', '')
        booking_notes = request.POST.get('booking_notes', '')

        # Calculate total amount (for now, free events)
        total_amount = 0.00

        # Create booking
        booking = EventBooking.objects.create(
            event=event,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            number_of_people=number_of_people,
            number_of_adults=number_of_adults,
            number_of_children=number_of_children,
            special_requirements=special_requirements,
            accessibility_needs=accessibility_needs,
            booking_notes=booking_notes,
            total_amount=total_amount,
            payment_status='confirmed' if total_amount == 0 else 'pending',
            user=request.user if request.user.is_authenticated else None,  # SECURITY FIX
        )
        
        # SECURITY FIX: For logged-in users, enforce their email
        if request.user.is_authenticated:
            booking.customer_email = request.user.email
            if not booking.customer_name and (request.user.first_name or request.user.last_name):
                booking.customer_name = f"{request.user.first_name} {request.user.last_name}".strip()
                if not booking.customer_name:
                    booking.customer_name = request.user.username
            booking.save()

        # Send confirmation email
        try:
            send_event_booking_confirmation_email(booking)
            messages.success(request, f'Your booking has been confirmed! Confirmation number: {booking.confirmation_number}')
        except Exception as e:
            messages.warning(request, f'Booking created but email failed to send. Confirmation: {booking.confirmation_number}')

        return redirect('bookings:event_booking_thanks', confirmation_number=booking.confirmation_number)

    context = {
        'event': event,
        'monastery': event.monastery,
    }
    return render(request, 'bookings/event_booking_form.html', context)


@login_required
def event_booking_thanks(request, confirmation_number):
    """
    Thank you page after successful event booking.
    """
    booking = get_object_or_404(EventBooking, confirmation_number=confirmation_number)

    context = {
        'booking': booking,
        'event': booking.event,
        'monastery': booking.event.monastery,
    }
    return render(request, 'bookings/event_booking_thanks.html', context)


@login_required
def event_booking_detail(request, confirmation_number):
    """
    Event booking detail view.
    """
    booking = get_object_or_404(EventBooking, confirmation_number=confirmation_number)

    context = {
        'booking': booking,
        'event': booking.event,
        'monastery': booking.event.monastery,
    }
    return render(request, 'bookings/event_booking_detail.html', context)


@login_required
def download_receipt(request, confirmation_number):
    """
    Download receipt for event booking as PDF.
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from io import BytesIO
    import os
    
    booking = get_object_or_404(EventBooking, confirmation_number=confirmation_number)
    
    # Security check - only allow user to download their own receipt
    if request.user.is_authenticated and booking.user and booking.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    # Create PDF buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        textColor=colors.HexColor('#1f2937'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#3b82f6'),
        spaceBefore=20
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("MONASTERY360 - BOOKING RECEIPT", title_style))
    story.append(Spacer(1, 20))
    
    # Confirmation details
    confirmation_data = [
        ['Confirmation Number:', booking.confirmation_number],
        ['Receipt Number:', booking.receipt_number],
        ['Date of Booking:', booking.created_at.strftime('%B %d, %Y at %I:%M %p')]
    ]
    
    confirmation_table = Table(confirmation_data, colWidths=[2*inch, 3*inch])
    confirmation_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(confirmation_table)
    story.append(Spacer(1, 20))
    
    # Customer Information
    story.append(Paragraph("CUSTOMER INFORMATION", heading_style))
    customer_data = [
        ['Name:', booking.customer_name],
        ['Email:', booking.customer_email],
        ['Phone:', booking.customer_phone]
    ]
    
    customer_table = Table(customer_data, colWidths=[2*inch, 3*inch])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 20))
    
    # Event Details
    story.append(Paragraph("EVENT DETAILS", heading_style))
    event_data = [
        ['Event:', booking.event.title],
        ['Date:', booking.event.start_time.strftime('%B %d, %Y')],
        ['Time:', booking.event.start_time.strftime('%I:%M %p')],
        ['Monastery:', booking.event.monastery.name],
        ['Address:', booking.event.monastery.address]
    ]
    
    event_table = Table(event_data, colWidths=[2*inch, 3*inch])
    event_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(event_table)
    story.append(Spacer(1, 20))
    
    # Booking Details
    story.append(Paragraph("BOOKING DETAILS", heading_style))
    booking_data = [
        ['Number of People:', str(booking.number_of_people)],
        ['Adults:', str(booking.number_of_adults)],
        ['Children:', str(booking.number_of_children)]
    ]
    
    booking_table = Table(booking_data, colWidths=[2*inch, 3*inch])
    booking_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(booking_table)
    story.append(Spacer(1, 20))
    
    # Payment Information
    story.append(Paragraph("PAYMENT INFORMATION", heading_style))
    payment_data = [
        ['Total Amount:', f"₹{booking.total_amount}" if booking.total_amount > 0 else 'Free'],
        ['Payment Status:', booking.get_payment_status_display()]
    ]
    
    payment_table = Table(payment_data, colWidths=[2*inch, 3*inch])
    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(payment_table)
    story.append(Spacer(1, 20))
    
    # Additional information
    if booking.special_requirements:
        story.append(Paragraph("SPECIAL REQUIREMENTS", heading_style))
        story.append(Paragraph(booking.special_requirements, styles['Normal']))
        story.append(Spacer(1, 15))
    
    if booking.accessibility_needs:
        story.append(Paragraph("ACCESSIBILITY NEEDS", heading_style))
        story.append(Paragraph(booking.accessibility_needs, styles['Normal']))
        story.append(Spacer(1, 15))
    
    if booking.booking_notes:
        story.append(Paragraph("NOTES", heading_style))
        story.append(Paragraph(booking.booking_notes, styles['Normal']))
        story.append(Spacer(1, 15))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you for booking with Monastery360!", styles['Normal']))
    story.append(Paragraph("Please present this receipt at the venue.", styles['Normal']))
    if booking.event.monastery.phone:
        story.append(Paragraph(f"For any queries, please contact: {booking.event.monastery.phone}", styles['Normal']))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Italic']))

    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.confirmation_number}.pdf"'
    
    return response


def send_event_booking_confirmation_email(booking):
    """
    Send confirmation email for event booking.
    """
    subject = f'Event Booking Confirmation - {booking.confirmation_number}'
    context = {
        'booking': booking,
        'event': booking.event,
        'monastery': booking.event.monastery,
    }

    html_message = render_to_string('bookings/emails/event_booking_confirmation.html', context)
    plain_message = render_to_string('bookings/emails/event_booking_confirmation.txt', context)

    send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.customer_email],
        fail_silently=False,
    )


@login_required
@require_http_methods(["POST"])
@login_required
def cancel_event_booking(request, confirmation_number):
    """
    Cancel an event booking if it belongs to the logged-in user.
    """
    print(f"DEBUG: Cancel request received for {confirmation_number}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: User: {request.user}, User email: {request.user.email}")

    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('core:profile')

    booking = get_object_or_404(EventBooking, confirmation_number=confirmation_number)
    print(f"DEBUG: Booking found - ID: {booking.id}, Status: {booking.payment_status}, Customer: {booking.customer_email}")

    # Check if the booking belongs to the current user
    if booking.customer_email != request.user.email:
        print(f"DEBUG: Email mismatch - Booking: {booking.customer_email}, User: {request.user.email}")
        messages.error(request, "You can only cancel your own bookings.")
        return redirect('core:profile')

    # Check if booking can be cancelled (not already completed/cancelled)
    if booking.payment_status in ['completed', 'cancelled']:
        print(f"DEBUG: Cannot cancel - status is {booking.payment_status}")
        messages.error(request, f"This booking cannot be cancelled. Current status: {booking.payment_status}")
        return redirect('core:profile')

    # Allow cancellation regardless of event timing
    # Users should be able to cancel bookings even for past events

    # Cancel the booking
    old_status = booking.payment_status
    booking.payment_status = 'cancelled'
    booking.admin_notes = f"Cancelled by user on {timezone.now()}"
    booking.save()

    messages.success(request, f"Your booking for '{booking.event.title}' has been cancelled successfully. Status changed from '{old_status}' to 'cancelled'.")

    # Send cancellation email
    try:
        send_cancellation_email(booking)
    except Exception as e:
        messages.warning(request, "Booking cancelled but confirmation email could not be sent.")

    return redirect('core:profile')


def send_cancellation_email(booking):
    """Send booking cancellation confirmation email."""
    subject = f"Booking Cancelled - {booking.event.title}"

    context = {
        'booking': booking,
        'event': booking.event,
        'monastery': booking.event.monastery,
    }

    # For now, send a simple email (you can create templates later)
    plain_message = f"""
Dear {booking.customer_name},

Your booking for "{booking.event.title}" has been successfully cancelled.

Booking Details:
- Confirmation Number: {booking.confirmation_number}
- Event: {booking.event.title}
- Date: {booking.event.start_time.strftime('%B %d, %Y at %I:%M %p')}
- Number of People: {booking.number_of_people}

If you have any questions, please contact us.

Best regards,
{booking.event.monastery.name}
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.customer_email],
        fail_silently=False,
    )


@login_required
def user_bookings_dashboard(request):
    """
    User dashboard showing all their bookings and event bookings.
    """
    # Get user's regular bookings
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Get user's event bookings
    user_event_bookings = EventBooking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user_bookings': user_bookings,
        'user_event_bookings': user_event_bookings,
        'page_title': 'My Bookings - Monastery360',
        'page_description': 'View and manage all your monastery visit bookings and event registrations',
    }
    
    return render(request, 'bookings/user_dashboard.html', context)


def download_booking_receipt(request, confirmation_number):
    """
    Download receipt for regular monastery booking as PDF.
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from io import BytesIO
    import os
    
    booking = get_object_or_404(Booking, confirmation_number=confirmation_number)
    
    # Security check - only allow user to download their own receipt
    if request.user.is_authenticated and booking.user and booking.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    # Create PDF buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        textColor=colors.HexColor('#1f2937'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#3b82f6'),
        spaceBefore=20
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("MONASTERY360 - VISIT BOOKING RECEIPT", title_style))
    story.append(Spacer(1, 20))
    
    # Confirmation details
    confirmation_data = [
        ['Confirmation Number:', booking.confirmation_number],
        ['Date of Booking:', booking.created_at.strftime('%B %d, %Y at %I:%M %p')]
    ]
    
    confirmation_table = Table(confirmation_data, colWidths=[2*inch, 3*inch])
    confirmation_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(confirmation_table)
    story.append(Spacer(1, 20))
    
    # Visitor Information
    story.append(Paragraph("VISITOR INFORMATION", heading_style))
    visitor_data = [
        ['Name:', booking.name],
        ['Email:', booking.email],
        ['Phone:', booking.phone],
        ['Preferred Language:', booking.preferred_language]
    ]
    
    visitor_table = Table(visitor_data, colWidths=[2*inch, 3*inch])
    visitor_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(visitor_table)
    story.append(Spacer(1, 20))
    
    # Visit Details
    story.append(Paragraph("VISIT DETAILS", heading_style))
    visit_data = [
        ['Monastery:', booking.monastery.name],
        ['Address:', booking.monastery.address],
        ['Visit Date:', booking.visit_date.strftime('%B %d, %Y')],
        ['Visit Time:', booking.visit_time.strftime('%I:%M %p') if booking.visit_time else 'To be confirmed'],
        ['Visit Type:', booking.get_visit_type_display()]
    ]
    
    visit_table = Table(visit_data, colWidths=[2*inch, 3*inch])
    visit_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(visit_table)
    story.append(Spacer(1, 20))
    
    # Group Information
    story.append(Paragraph("GROUP INFORMATION", heading_style))
    group_data = [
        ['Number of Visitors:', str(booking.number_of_visitors)],
        ['Adults:', str(booking.number_of_adults)],
        ['Children:', str(booking.number_of_children)]
    ]
    
    group_table = Table(group_data, colWidths=[2*inch, 3*inch])
    group_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(group_table)
    story.append(Spacer(1, 20))
    
    # Organization details (if applicable)
    if booking.organization:
        story.append(Paragraph("ORGANIZATION DETAILS", heading_style))
        org_data = [
            ['Organization:', booking.organization],
            ['Group Leader:', booking.group_leader if booking.group_leader else 'Not specified']
        ]
        
        org_table = Table(org_data, colWidths=[2*inch, 3*inch])
        org_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(org_table)
        story.append(Spacer(1, 20))
    
    # Services
    story.append(Paragraph("SERVICES", heading_style))
    services_data = [
        ['Transportation Needed:', 'Yes' if booking.transportation_needed else 'No'],
        ['Accommodation Needed:', 'Yes' if booking.accommodation_needed else 'No'],
        ['Booking Status:', booking.get_status_display()]
    ]
    
    services_table = Table(services_data, colWidths=[2*inch, 3*inch])
    services_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(services_table)
    story.append(Spacer(1, 20))
    
    # Additional information
    if booking.purpose_of_visit:
        story.append(Paragraph("PURPOSE OF VISIT", heading_style))
        story.append(Paragraph(booking.purpose_of_visit, styles['Normal']))
        story.append(Spacer(1, 15))
    
    if booking.special_requirements:
        story.append(Paragraph("SPECIAL REQUIREMENTS", heading_style))
        story.append(Paragraph(booking.special_requirements, styles['Normal']))
        story.append(Spacer(1, 15))
    
    if booking.notes:
        story.append(Paragraph("NOTES", heading_style))
        story.append(Paragraph(booking.notes, styles['Normal']))
        story.append(Spacer(1, 15))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you for choosing Monastery360!", styles['Normal']))
    story.append(Paragraph("For any queries, please contact the monastery directly or use your confirmation number.", styles['Normal']))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Italic']))

    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_receipt_{booking.confirmation_number}.pdf"'
    
    return response
