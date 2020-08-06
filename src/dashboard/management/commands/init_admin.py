from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
       print("Initial Auth Set Up")

       if not User.objects.filter(username="admin").exists():
           user = User.objects.create(username="admin")
           user.set_password("ab34cd12")
           user.is_staff = True
           user.is_superuser=True
           user.save()

       print("Created Admin user")
