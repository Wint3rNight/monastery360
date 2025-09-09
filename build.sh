#!/bin/bash
set -e

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements-minimal.txt

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
count = Monastery.objects.count()
print(f'Current monastery count: {count}')
if count == 0:
    print('Loading data...')
    from django.core.management import call_command
    try:
        call_command('loaddata', 'local_data.json')
        print('Data loaded successfully!')
    except Exception as e:
        print(f'Data loading failed: {e}')
else:
    print('Data already exists, skipping...')
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
