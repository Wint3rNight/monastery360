#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # exit on error

echo "Starting build process..."

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (use production requirements without GDAL)
echo "Installing Python dependencies..."
pip install -r requirements-render.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
