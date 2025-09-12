# Deployment Instructions for Monastery360

## Critical Fix for Production Issues

### 1. Receipt Download Fix

The receipt download functionality requires the `reportlab` library for PDF generation.

**Action Required:**

```bash
pip install reportlab==4.0.4
```

Or update from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Media Files Serving Fix

Archive downloads (PDF files) need proper media serving in production.

**For Render.com or similar platforms:**

-   The Django app now serves media files directly (not recommended for high-traffic, but works for moderate usage)
-   For better performance, configure a CDN or cloud storage (AWS S3, Cloudinary, etc.)

**For nginx/apache deployments:**
Configure your web server to serve media files directly:

```nginx
# nginx example
location /media/ {
    alias /path/to/your/project/media/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Environment Variables

Ensure these are set in production:

-   `DEBUG=False`
-   `ALLOWED_HOSTS` includes your domain
-   Database settings are correctly configured

### 4. Static Files

Run collectstatic after deployment:

```bash
python manage.py collectstatic --noinput
```

### 5. Dependencies Update

The requirements.txt now includes reportlab. Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Testing the Fixes

1. **Receipt Download**: Try downloading a receipt from a booking
2. **Archive Download**: Try downloading an archive file from the archives section
3. Both should work without 500 errors

## Troubleshooting

If you still get errors:

1. Check server logs for specific error messages
2. Ensure reportlab is installed: `python -c "import reportlab; print('OK')"`
3. Verify media files exist in the media directory
4. Check file permissions on media directory
