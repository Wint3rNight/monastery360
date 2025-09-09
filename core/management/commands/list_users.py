from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'List all users in the database'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('-date_joined')
        
        self.stdout.write(
            self.style.SUCCESS(f'Total users: {users.count()}\n')
        )
        
        for user in users:
            self.stdout.write(
                f"ID: {user.id} | Username: {user.username} | "
                f"Email: {user.email} | Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')} | "
                f"Last Login: {user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'}"
            )
