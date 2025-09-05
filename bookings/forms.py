"""
Forms for the bookings app.

Handles visitor booking forms with validation and custom widgets.
"""

from datetime import date, timedelta

from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Fieldset, Layout, Row, Submit
from django import forms
from django.utils import timezone

from core.models import Monastery

from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form for creating visitor bookings.

    Includes validation for visit dates, group sizes, and required fields.
    """

    class Meta:
        model = Booking
        fields = [
            'monastery', 'name', 'email', 'phone',
            'visit_date', 'visit_time', 'visit_type',
            'number_of_visitors', 'number_of_adults', 'number_of_children',
            'purpose_of_visit', 'special_requirements',
            'preferred_language', 'organization', 'group_leader',
            'transportation_needed', 'accommodation_needed', 'notes'
        ]

        widgets = {
            'visit_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().isoformat(),
                    'max': (date.today() + timedelta(days=365)).isoformat(),
                    'class': 'form-control'
                }
            ),
            'visit_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'purpose_of_visit': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Please describe the purpose of your visit...'
                }
            ),
            'special_requirements': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Any accessibility needs, dietary requirements, or special considerations...'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': 'Any additional information or questions...'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': '+91-XXXXXXXXXX'
                }
            ),
            'organization': forms.TextInput(
                attrs={
                    'placeholder': 'School, University, Company, etc.'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter active monasteries only
        self.fields['monastery'].queryset = Monastery.objects.filter(is_active=True).order_by('name')

        # Set field labels and help texts
        self.fields['name'].label = 'Full Name'
        self.fields['name'].help_text = 'Name of the primary contact person'

        self.fields['email'].help_text = 'We will send confirmation and details to this email'

        self.fields['phone'].help_text = 'Include country code (e.g., +91 for India)'

        self.fields['visit_date'].help_text = 'Please choose a date at least 3 days in advance'

        self.fields['visit_time'].help_text = 'Preferred time (optional - we will confirm availability)'
        self.fields['visit_time'].required = False

        self.fields['number_of_visitors'].help_text = 'Total number of people in your group'

        self.fields['number_of_adults'].help_text = 'Number of adults (18+ years)'

        self.fields['number_of_children'].help_text = 'Number of children (under 18 years)'
        self.fields['number_of_children'].required = False

        self.fields['preferred_language'].help_text = 'Language for communication during the visit'

        self.fields['organization'].required = False
        self.fields['group_leader'].required = False
        self.fields['group_leader'].help_text = 'If different from primary contact'

        self.fields['transportation_needed'].help_text = 'Check if you need help with transportation arrangements'
        self.fields['accommodation_needed'].help_text = 'Check if you need accommodation recommendations'

        # Set up crispy forms layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Monastery Selection',
                'monastery',
            ),
            Fieldset(
                'Contact Information',
                Row(
                    Column('name', css_class='form-group col-md-6'),
                    Column('email', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('phone', css_class='form-group col-md-6'),
                    Column('preferred_language', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Visit Details',
                Row(
                    Column('visit_date', css_class='form-group col-md-6'),
                    Column('visit_time', css_class='form-group col-md-6'),
                ),
                'visit_type',
                Row(
                    Column('number_of_visitors', css_class='form-group col-md-4'),
                    Column('number_of_adults', css_class='form-group col-md-4'),
                    Column('number_of_children', css_class='form-group col-md-4'),
                ),
                'purpose_of_visit',
            ),
            Fieldset(
                'Group Information (Optional)',
                Row(
                    Column('organization', css_class='form-group col-md-6'),
                    Column('group_leader', css_class='form-group col-md-6'),
                ),
                css_class='border-top pt-3 mt-3'
            ),
            Fieldset(
                'Additional Requirements',
                'special_requirements',
                Row(
                    Column('transportation_needed', css_class='form-group col-md-6'),
                    Column('accommodation_needed', css_class='form-group col-md-6'),
                ),
                'notes',
                css_class='border-top pt-3 mt-3'
            ),
            HTML('<div class="alert alert-info mt-3"><i class="fas fa-info-circle"></i> Your booking request will be reviewed and confirmed within 24-48 hours. You will receive an email confirmation with further details.</div>'),
            Submit('submit', 'Submit Booking Request', css_class='btn btn-primary btn-lg mt-3')
        )

    def clean_visit_date(self):
        """Validate visit date is not in the past and not too far in future."""
        visit_date = self.cleaned_data.get('visit_date')

        if visit_date:
            today = date.today()
            min_date = today + timedelta(days=2)  # At least 2 days in advance
            max_date = today + timedelta(days=365)  # Within one year

            if visit_date < min_date:
                raise forms.ValidationError(
                    f'Please choose a date at least 2 days in advance. Earliest available: {min_date.strftime("%B %d, %Y")}'
                )

            if visit_date > max_date:
                raise forms.ValidationError(
                    f'Bookings can only be made up to one year in advance. Latest date: {max_date.strftime("%B %d, %Y")}'
                )

        return visit_date

    def clean(self):
        """Validate form data consistency."""
        cleaned_data = super().clean()

        number_of_visitors = cleaned_data.get('number_of_visitors')
        number_of_adults = cleaned_data.get('number_of_adults', 0)
        number_of_children = cleaned_data.get('number_of_children', 0)

        # Validate visitor numbers add up
        if number_of_visitors and (number_of_adults + number_of_children) != number_of_visitors:
            raise forms.ValidationError(
                'The total number of visitors must equal the sum of adults and children.'
            )

        # Ensure at least one adult
        if number_of_adults == 0:
            raise forms.ValidationError(
                'At least one adult must be included in the group.'
            )

        # Validate group leader is provided for groups > 5
        if number_of_visitors and number_of_visitors > 5:
            organization = cleaned_data.get('organization')
            if not organization:
                self.add_error('organization', 'Organization name is required for groups larger than 5 people.')

        return cleaned_data


class BookingSearchForm(forms.Form):
    """
    Form for searching/filtering bookings in admin views.
    """

    confirmation_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter confirmation number',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email address',
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter phone number',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('confirmation_number', css_class='form-group col-md-4'),
                Column('email', css_class='form-group col-md-4'),
                Column('phone', css_class='form-group col-md-4'),
            ),
            Submit('search', 'Search Booking', css_class='btn btn-outline-primary')
        )
