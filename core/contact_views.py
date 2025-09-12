"""
Contact and Feedback views for Monastery360.
"""

import json

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import ContactSubmission, Feedback


def contact_page(request):
    """Contact page with phone and email information."""
    context = {
        'page_title': 'Contact Us - Monastery360',
        'page_description': 'Get in touch with Monastery360 team for support, partnerships, or general inquiries.',
        'contact_phone': '9153014860',
        'contact_email': 'pratap2003singh@gmail.com',
    }
    return render(request, 'core/contact.html', context)


@require_http_methods(["POST"])
def submit_contact(request):
    """Handle contact form submission."""
    try:
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'general')
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)

        # Create contact submission
        contact = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            user=request.user if request.user.is_authenticated else None
        )

        # Send notification email to admin
        try:
            admin_subject = f'New Contact Form Submission - {contact.get_subject_display()}'
            admin_message = f"""
New contact form submission received:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {contact.get_subject_display()}

Message:
{message}

Submission ID: {contact.id}
Submitted at: {contact.created_at}
"""

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['pratap2003singh@gmail.com'],
                fail_silently=True,  # Don't fail if email doesn't work
            )
        except Exception:
            pass  # Continue even if email fails

        return JsonResponse({
            'success': True,
            'message': 'Thank you for contacting us! We\'ll get back to you within 24-48 hours.'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'There was an error submitting your message. Please try again or contact us directly.'
        }, status=500)


def feedback_page(request):
    """Feedback page for user reviews and suggestions."""
    # Redirect unregistered users to login
    if not request.user.is_authenticated:
        from django.contrib.auth.decorators import login_required
        from django.shortcuts import redirect
        return redirect('core:login')

    context = {
        'page_title': 'Feedback - Monastery360',
        'page_description': 'Share your experience and help us improve Monastery360.',
    }
    return render(request, 'core/feedback.html', context)


@require_http_methods(["POST"])
def submit_feedback(request):
    """Handle feedback form submission."""
    # Redirect unregistered users to login
    if not request.user.is_authenticated:
        return redirect('core:login')

    try:
        # Get form data
        subject = request.POST.get('subject', 'general')
        message = request.POST.get('message', '').strip()

        # For logged-in users, use their profile info
        name = request.user.get_full_name() or request.user.username
        email = request.user.email

        # Basic validation
        if not message:
            messages.error(request, 'Please provide your feedback message.')
            return redirect('core:feedback')

        # Create feedback entry
        feedback = Feedback.objects.create(
            name=name,
            email=email,
            category=subject,
            title=f"{subject.replace('_', ' ').title()} from {name}",
            message=message,
            user=request.user,
            browser_info=request.META.get('HTTP_USER_AGENT', '')[:500]
        )

        # Send notification email to admin
        try:
            admin_subject = f'New Feedback: {subject.replace("_", " ").title()} - Monastery360'
            admin_message = f"""
New feedback received from {name}:

Subject: {subject.replace('_', ' ').title()}
Email: {email}
Message:

{message}

---
Feedback ID: {feedback.id}
Submitted: {feedback.created_at}
User Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}
"""

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['pratap2003singh@gmail.com'],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, 'Thank you for your feedback! We really appreciate your input and will use it to improve Monastery360.')
        return redirect('core:feedback')

    except Exception as e:
        messages.error(request, 'There was an error submitting your feedback. Please try again or contact us directly.')
        return redirect('core:feedback')


def about_page(request):
    """About page with mission and team information."""
    context = {
        'page_title': 'About Us - Monastery360',
        'page_description': 'Learn about our mission to preserve and share Buddhist heritage through digital innovation.',
    }
    return render(request, 'core/about.html', context)


def resources_page(request):
    """Resources page with helpful links and information."""
    context = {
        'page_title': 'Resources - Monastery360',
        'page_description': 'Access helpful resources about Buddhism, meditation, and monastery visits.',
    }
    return render(request, 'core/resources.html', context)
