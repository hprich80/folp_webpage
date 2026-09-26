import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update the prototype admin using DEMO_ADMIN_USERNAME/PASSWORD.'

    def handle(self, *args, **options):
        username = os.environ.get('DEMO_ADMIN_USERNAME')
        password = os.environ.get('DEMO_ADMIN_PASSWORD')
        if not username or not password:
            raise CommandError('Set DEMO_ADMIN_USERNAME and DEMO_ADMIN_PASSWORD.')
        user, _ = get_user_model().objects.get_or_create(username=username)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS('Prototype administrator configured.'))
