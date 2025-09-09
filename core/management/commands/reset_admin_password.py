from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reset admin password to a known value'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Username to reset')
        parser.add_argument('--password', required=True, help='New password')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully reset password for user "{username}" and made them superuser')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
