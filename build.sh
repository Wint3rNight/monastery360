#!/bin/bash
# Build script for Render deployment
set -e

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies from requirements-render.txt..."
pip install -r requirements-render.txt

# Verify Django installation
python -c "import django; print(f'Django {django.get_version()} installed successfully')"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
