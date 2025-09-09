import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load local data fixtures into production database'

    def handle(self, *args, **options):
        # Check if we're in production (has DATABASE_URL)
        if not os.environ.get('DATABASE_URL'):
            self.stdout.write(
                self.style.WARNING('This command should only be run in production')
            )
            return

        self.stdout.write('Loading monastery and core app data...')
        try:
            call_command('loaddata', 'local_data.json')
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded local_data.json')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading local_data.json: {e}')
            )

        # Optional: Load users (you might skip this if you want fresh users)
        self.stdout.write('Loading user data...')
        try:
            call_command('loaddata', 'users_data.json')
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded users_data.json')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading users_data.json: {e}')
            )

        self.stdout.write(
            self.style.SUCCESS('Data migration complete!')
        )
