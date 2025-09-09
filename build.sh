#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # exit on error

echo "Starting build process..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies (use production requirements without GDAL)
echo "Installing Python dependencies..."
pip install -r requirements-render.txt

# Verify critical packages
echo "Verifying installations..."
python -c "import django; print(f'Django {django.get_version()}')"
python -c "import gunicorn; print('Gunicorn installed')"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Check for any Django configuration issues
echo "Running Django system checks..."
python manage.py check --deploy

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
