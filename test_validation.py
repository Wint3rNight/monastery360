#!/usr/bin/env python3
"""
Test script for username/email uniqueness validation
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/winter/Documents/Workspace2/monastery360')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from core.auth_views import CustomUserCreationForm

def test_validation():
    print("=== Testing Username/Email Uniqueness Validation ===\n")
    
    # Get existing users
    users = User.objects.all()[:3]  # Get first 3 users
    print(f"Found {User.objects.count()} existing users in database")
    
    if users:
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.username} ({user.email})")
    
    print("\n" + "="*50)
    
    if users:
        test_user = users[0]
        print(f"\nTesting with existing user: {test_user.username} ({test_user.email})")
        
        # Test 1: Duplicate username with different case
        print("\n1. Testing duplicate username (different case)...")
        form_data = {
            'username': test_user.username.upper(),  # Different case
            'email': 'newemail@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        form = CustomUserCreationForm(data=form_data)
        is_valid = form.is_valid()
        print(f"   Form valid: {is_valid}")
        if not is_valid:
            print(f"   Errors: {dict(form.errors)}")
        
        # Test 2: Duplicate email with different case
        print("\n2. Testing duplicate email (different case)...")
        form_data = {
            'username': 'newusername123',
            'email': test_user.email.upper(),  # Different case
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        form = CustomUserCreationForm(data=form_data)
        is_valid = form.is_valid()
        print(f"   Form valid: {is_valid}")
        if not is_valid:
            print(f"   Errors: {dict(form.errors)}")
        
        # Test 3: Valid new user
        print("\n3. Testing valid new user...")
        form_data = {
            'username': 'newvaliduser123',
            'email': 'newvalid@test.com',
            'first_name': 'Valid',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        form = CustomUserCreationForm(data=form_data)
        is_valid = form.is_valid()
        print(f"   Form valid: {is_valid}")
        if not is_valid:
            print(f"   Errors: {dict(form.errors)}")
        
    else:
        print("No existing users found - cannot test duplicate validation")
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == '__main__':
    test_validation()
