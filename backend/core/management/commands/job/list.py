from django.core.management.base import BaseCommand
from django_q.models import OrmQ

class Command(BaseCommand):
    help = 'List all queued jobs'

    def handle(self, *args, **options):
        jobs = OrmQ.objects.all()
        if not jobs:
            self.stdout.write(self.style.WARNING('No jobs in the queue.'))
        else:
            for job in jobs:
                self.stdout.write(f'Job ID: {job.id}, Task: {job.func}')