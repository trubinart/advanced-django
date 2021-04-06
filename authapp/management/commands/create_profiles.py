from django.core.management.base import BaseCommand
from authapp.models import Users, UsersProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in Users.objects.filter(usersprofile__isnull=True):
            UsersProfile.objects.create(user=user)
