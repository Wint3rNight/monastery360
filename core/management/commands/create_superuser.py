import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a superuser for production'

    def handle(self, *args, **options):
        username = os.environ.get('SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@monastery360.com')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write(
                self.style.ERROR('SUPERUSER_PASSWORD environment variable not set')
            )
            return

        # Check if user exists and update if needed
        try:
            user = User.objects.get(username=username)
            if not user.is_superuser or not user.is_staff:
                # Update existing user to be superuser
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                user.email = email
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated existing user "{username}" to superuser')
                )
            else:
                # Reset password for existing superuser
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Reset password for existing superuser "{username}"')
                )
        except User.DoesNotExist:
            # Create new superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
