#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies (use production requirements without GDAL)
pip install -r requirements-render.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
