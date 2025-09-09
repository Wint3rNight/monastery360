#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements-minimal.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Build complete!"
