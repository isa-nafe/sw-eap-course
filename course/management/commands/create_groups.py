from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates Student and Instructor groups'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Students')
        Group.objects.get_or_create(name='Instructors')
        self.stdout.write(self.style.SUCCESS('Successfully created Students and Instructors groups'))
