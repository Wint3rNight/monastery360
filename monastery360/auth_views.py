import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    """Render the login/signup page"""
    context = {
        'FIREBASE_API_KEY': os.getenv('FIREBASE_API_KEY', 'your-api-key-here'),
        'FIREBASE_AUTH_DOMAIN': os.getenv('FIREBASE_AUTH_DOMAIN', 'your-project.firebaseapp.com'),
        'FIREBASE_PROJECT_ID': os.getenv('FIREBASE_PROJECT_ID', 'your-project-id'),
        'FIREBASE_STORAGE_BUCKET': os.getenv('FIREBASE_STORAGE_BUCKET', 'your-project.appspot.com'),
        'FIREBASE_MESSAGING_SENDER_ID': os.getenv('FIREBASE_MESSAGING_SENDER_ID', '123456789'),
        'FIREBASE_APP_ID': os.getenv('FIREBASE_APP_ID', 'your-app-id'),
    }
    return render(request, 'auth/login.html', context)

def signup_view(request):
    """Render the signup page (same template as login)"""
    context = {
        'FIREBASE_API_KEY': os.getenv('FIREBASE_API_KEY', 'your-api-key-here'),
        'FIREBASE_AUTH_DOMAIN': os.getenv('FIREBASE_AUTH_DOMAIN', 'your-project.firebaseapp.com'),
        'FIREBASE_PROJECT_ID': os.getenv('FIREBASE_PROJECT_ID', 'your-project-id'),
        'FIREBASE_STORAGE_BUCKET': os.getenv('FIREBASE_STORAGE_BUCKET', 'your-project.appspot.com'),
        'FIREBASE_MESSAGING_SENDER_ID': os.getenv('FIREBASE_MESSAGING_SENDER_ID', '123456789'),
        'FIREBASE_APP_ID': os.getenv('FIREBASE_APP_ID', 'your-app-id'),
    }
    return render(request, 'auth/login.html', context)

@csrf_exempt
def auth_callback(request):
    """Handle authentication callbacks from Firebase"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Handle user data from Firebase
            # You can process the user data here if needed
            return JsonResponse({'status': 'success', 'message': 'User authenticated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
