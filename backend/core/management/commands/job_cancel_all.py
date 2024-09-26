from django.core.management.base import BaseCommand
from django_q.models import OrmQ


class Command(BaseCommand):
    help = 'Cancel all queued jobs'

    def handle(self, *args, **options):
        count = OrmQ.objects.all().count()
        OrmQ.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Cancelled {count} jobs.'))
