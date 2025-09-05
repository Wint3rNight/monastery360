"""
Content Security Policy configuration for Monastery360.

This file defines CSP directives to enhance security by controlling
which resources the browser is allowed to load.
"""

# Content Security Policy settings
CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",  # Required for some inline scripts
    "https://unpkg.com",  # CDN for Leaflet and other libraries
    "https://cdn.jsdelivr.net",  # CDN for libraries
    "https://cdnjs.cloudflare.com",  # CDN for libraries
)

CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",  # Required for inline styles
    "https://unpkg.com",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://fonts.googleapis.com",
)

CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com",
    "data:",
)

CSP_IMG_SRC = (
    "'self'",
    "data:",
    "https:",  # Allow images from any HTTPS source
    "blob:",   # For generated images
)

CSP_CONNECT_SRC = (
    "'self'",
    "https:",  # Allow API calls to external services
)

CSP_FRAME_SRC = (
    "'self'",
)

CSP_OBJECT_SRC = ("'none'",)

CSP_BASE_URI = ("'self'",)

CSP_FORM_ACTION = ("'self'",)

CSP_FRAME_ANCESTORS = ("'none'",)

# Service Worker
CSP_WORKER_SRC = ("'self'",)
