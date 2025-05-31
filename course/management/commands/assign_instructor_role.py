from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import os

class Command(BaseCommand):
    help = "Assigns the 'Instructors' group to the user specified by DJANGO_SUPERUSER_USERNAME"

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'instructor')
        try:
            user = User.objects.get(username=username)
            instructors_group, created = Group.objects.get_or_create(name='Instructors')
            user.groups.add(instructors_group)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' successfully assigned to 'Instructors' group."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' not found. Please create it first."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
