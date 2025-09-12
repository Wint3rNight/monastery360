#!/bin/bash
set -e

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements-render.txt

echo "=== Verifying Django installation ==="
python -c "import django; print(f'Django {django.get_version()}')"
python -c "import environ; print('django-environ OK')"

echo "=== Testing database connection ==="
python manage.py check --database default

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear || echo "Static files collection had issues but continuing..."

echo "=== Running migrations ==="
python manage.py migrate

echo "=== Creating superuser if needed ==="
python manage.py create_superuser || echo "Superuser creation skipped (may already exist)"

echo "=== Loading production data (if needed) ==="
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monastery360.settings')
django.setup()
from core.models import Monastery
from bookings.models import Booking
from tours.models import Panorama
from events.models import Event

monastery_count = Monastery.objects.count()
booking_count = Booking.objects.count()
tour_count = Panorama.objects.count()
event_count = Event.objects.count()

print(f'Current data counts:')
print(f'- Monasteries: {monastery_count}')
print(f'- Events: {event_count}')
print(f'- Tours: {tour_count}')
print(f'- Bookings: {booking_count}')

if monastery_count == 0 or event_count == 0 or tour_count == 0:
    print('Missing data detected, loading from fixtures...')
    from django.core.management import call_command
    try:
        call_command('load_production_data')
        print('✅ All data loaded successfully!')
    except Exception as e:
        print(f'❌ Data loading failed: {e}')
else:
    print('✅ Data already exists, skipping data load...')
"

echo "=== Checking if User model works ==="
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monastery360.settings')
django.setup()
from django.contrib.auth.models import User
print(f'User model working. Total users: {User.objects.count()}')
"

echo "=== Creating superuser if needed ==="
python manage.py create_superuser || echo "Superuser creation skipped or failed"

echo "=== Build complete! ==="
