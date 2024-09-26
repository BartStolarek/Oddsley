from django.core.management.base import BaseCommand
from django_q.models import OrmQ


class Command(BaseCommand):
    help = 'Cancel a queued job'

    def add_arguments(self, parser):
        parser.add_argument('job_id', type=str, help='ID of the job to cancel')

    def handle(self, *args, **options):
        job_id = options['job_id']
        try:
            job = OrmQ.objects.get(id=job_id)
            job.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Job {job_id} cancelled successfully.'))
        except OrmQ.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'No job found with ID: {job_id}'))
