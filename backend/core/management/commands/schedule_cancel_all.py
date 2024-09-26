from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Cancel all scheduled tasks'

    def handle(self, *args, **options):
        scheduled_tasks = Schedule.objects.all()
        count = scheduled_tasks.count()

        if count == 0:
            self.stdout.write(self.style.WARNING('No scheduled tasks found.'))
            return

        scheduled_tasks.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully cancelled all {count} scheduled tasks.'))
