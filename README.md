# Monastery360

A comprehensive digital platform for exploring and preserving the rich heritage of Sikkim's monasteries. Built for the Smart India Hackathon, this Django web application provides virtual tours, historical archives, event management, and visitor booking capabilities.

## Key Features

-   **Interactive Maps**: GeoDjango-powered mapping with monastery locations and audio points of interest
-   **Virtual Tours**: 360-degree panoramic views using Pannellum
-   **Digital Archives**: Historical manuscripts, artifacts, and documents with search capabilities
-   **Event Calendar**: Public events and festivals with monastery-specific filtering
-   **Visitor Booking**: Simple form-based visit scheduling system
-   **Progressive Web App**: Installable, offline-capable web application
-   **Multilingual Support**: English, Hindi, and Nepali language support
-   **Accessibility First**: WCAG-compliant interface with semantic HTML and ARIA roles

## Quick start (development)

Prerequisites

-   Python 3.11+
-   Git
-   System libs for GeoDjango (GDAL, GEOS, PROJ) if you use spatial features

Minimal setup

```bash
git clone <repository-url>
cd monastery360

# Create and activate a venv (fish shell example)
python3 -m venv .venv
source .venv/bin/activate.fish

pip install --upgrade pip
pip install -r requirements.txt

# copy env template and edit local values
cp .env.example .env

python manage.py migrate
# optional: python manage.py load_demo

python manage.py runserver
```

Open http://localhost:8000

## Tests & quality

Run tests

```bash
python manage.py test
```

Lint & format

```bash
flake8 .
black .
isort .
```

## Project structure (high level)

```
monastery360/
├── core/        # app: models, views, templates
├── tours/       # virtual tours + panoramas
├── archives/    # archive models and views
├── events/      # event calendar
├── bookings/    # visitor booking
├── api/         # REST endpoints
├── static/      # front-end assets
├── templates/   # HTML templates
└── requirements.txt
```

## Environment

Copy `.env.example` to `.env` and set values such as `SECRET_KEY`, `ALLOWED_HOSTS`, database or storage credentials.

Important: never commit `.env` or other secret files. This repo's `.gitignore` already includes common local files (venv, .env, logs, backups).

CI note: the GitHub Actions workflow installs the system `python3-gdal` package and excludes `GDAL` from the pip requirements to avoid building GDAL from source inside the runner; when contributing, install system GDAL (and GEOS/PROJ) locally if you use spatial features.

## Pushing to GitHub

Create a remote and push (one-time):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:<your-username>/monastery360.git
git push -u origin main
```

Add a `LICENSE` and `CONTRIBUTING.md` before publishing if you plan to open-source this repository.

## Notes

-   If you committed secrets earlier, rotate them (API keys, tokens).
-   Large media and upload directories should be stored outside git (cloud storage or release assets).
-   If you use spatial features locally, install system libraries first (GDAL, GEOS, PROJ, SpatiaLite or PostGIS).

## License

Add a `LICENSE` file (MIT/Apache recommended) and update this README accordingly.
