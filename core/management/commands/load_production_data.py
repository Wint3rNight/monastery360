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
        
        # List of data files to load in order (dependencies first)
        data_files = [
            ('local_data.json', 'Core app data (monasteries, audio POIs)'),
            ('events_data.json', 'Events data'),
            ('tours_data.json', 'Tours and panorama data'),
            ('bookings_data.json', 'Booking data'),
            ('users_data.json', 'User data'),
        ]
        
        for filename, description in data_files:
            self.stdout.write(f'Loading {description}...')
            try:
                call_command('loaddata', filename)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Successfully loaded {filename}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error loading {filename}: {e}')
                )
                # Continue with other files even if one fails
                continue
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Data migration complete!')
        )
        
        # Show summary
        self.stdout.write('\n📊 Checking data counts...')
        try:
            from django.contrib.auth.models import User
            from core.models import Monastery
            from tours.models import Panorama
            from bookings.models import Booking
            from events.models import Event
            
            self.stdout.write(f'Users: {User.objects.count()}')
            self.stdout.write(f'Monasteries: {Monastery.objects.count()}')
            self.stdout.write(f'Events: {Event.objects.count()}')
            self.stdout.write(f'Panoramas: {Panorama.objects.count()}')
            self.stdout.write(f'Bookings: {Booking.objects.count()}')
            
        except Exception as e:
            self.stdout.write(f'Could not show summary: {e}')
