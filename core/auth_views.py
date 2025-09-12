"""
Authentication views for Monastery360.

Handles user registration, login, logout, and profile management.
"""

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields."""

    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if email:
            # Convert to lowercase for case-insensitive comparison
            email = email.lower()
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        """Ensure username is unique and valid."""
        username = self.cleaned_data.get('username')
        if username:
            # Convert to lowercase for case-insensitive comparison
            username = username.lower()
            if User.objects.filter(username__iexact=username).exists():
                raise ValidationError("A user with this username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form that allows login with email or username."""

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username

        # Check if the input is an email
        if '@' in username:
            try:
                # Try to find user by email
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                # If no user found with this email, return the original input
                # Django's authenticate will handle the failure
                return username

        return username


def _handle_login(request, login_form):
    """Handle user login logic."""
    if not login_form.is_valid():
        messages.error(request, 'Please correct the errors below.')
        return None
    
    username = login_form.cleaned_data['username']
    password = login_form.cleaned_data['password']
    
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        next_url = request.GET.get('next', reverse('core:home'))
        return redirect(next_url)
    else:
        messages.error(request, 'Invalid username/email or password.')
        return None


def _validate_user_uniqueness(request, username, email, login_form, signup_form):
    """Validate that username and email are unique."""
    if User.objects.filter(username__iexact=username).exists():
        messages.error(request, f'Username "{username}" is already taken. Please choose a different username.')
        return render(request, 'auth/login_test.html', {
            'login_form': login_form,
            'signup_form': signup_form,
            'show_signup': True,
        })
    
    if User.objects.filter(email__iexact=email).exists():
        messages.error(request, f'An account with email "{email}" already exists. Please use a different email or try logging in.')
        return render(request, 'auth/login_test.html', {
            'login_form': login_form,
            'signup_form': signup_form,
            'show_signup': True,
        })
    
    return None


def _handle_signup(request, signup_form, login_form):
    """Handle user signup logic."""
    if not signup_form.is_valid():
        for field, errors in signup_form.errors.items():
            for error in errors:
                messages.error(request, f'{field.replace("_", " ").title()}: {error}')
        return None
    
    try:
        username = signup_form.cleaned_data['username'].lower()
        email = signup_form.cleaned_data['email'].lower()
        
        # Check uniqueness
        uniqueness_response = _validate_user_uniqueness(request, username, email, login_form, signup_form)
        if uniqueness_response:
            return uniqueness_response
        
        # Ensure we're not already logged in
        if request.user.is_authenticated:
            logout(request)
        
        # Create the user
        user = signup_form.save()
        
        if user and user.pk:
            created_user = User.objects.get(pk=user.pk)
            login(request, created_user)
            messages.success(request, f'Welcome to Monastery360, {created_user.first_name}! Your account "{created_user.username}" has been created successfully.')
            return redirect('core:home')
        else:
            messages.error(request, 'Account creation failed. Please try again.')
    except Exception as e:
        messages.error(request, f'Account creation failed: {str(e)}')
    
    return None


def login_view(request):
    """Handle user login and registration."""
    if request.user.is_authenticated:
        return redirect('core:home')

    login_form = CustomAuthenticationForm()
    signup_form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(data=request.POST)
            result = _handle_login(request, login_form)
            if result:
                return result
        elif 'signup_submit' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            result = _handle_signup(request, signup_form, login_form)
            if result:
                return result

    return render(request, 'auth/login_test.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'show_signup': request.GET.get('signup') == 'true',
    })


@require_http_methods(["POST"])
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('core:home')


def signup_redirect(request):
    """Redirect to login page with signup form active."""
    return redirect('core:login' + '?signup=true')


@login_required
def profile_view(request):
    """User profile view with bookings."""
    from bookings.models import EventBooking

    # Get user's event bookings
    user_bookings = EventBooking.objects.filter(
        customer_email=request.user.email
    ).select_related('event', 'event__monastery').order_by('-created_at')

    return render(request, 'auth/profile.html', {
        'user': request.user,
        'bookings': user_bookings,
    })


@login_required
@require_http_methods(["POST"])
def profile_update_view(request):
    """Handle profile updates."""
    try:
        user = request.user

        # Update user fields
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Validate email uniqueness (excluding current user)
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

        # Update user fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
