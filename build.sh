#!/bin/bash
set -e

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements-minimal.txt

echo "=== Verifying Django installation ==="
python -c "import django; print(f'Django {django.get_version()}')"
python -c "import environ; print('django-environ OK')"

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Running migrations ==="
python manage.py migrate

echo "=== Build complete! ==="
