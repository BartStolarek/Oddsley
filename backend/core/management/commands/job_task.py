from django.core.management.base import BaseCommand
from django_q.tasks import async_task
import uuid


class Command(BaseCommand):
    help = 'Queue a job with a specified task'

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='Name of the task to queue')
        parser.add_argument('--args', nargs='*', help='Optional arguments for the task')

    def handle(self, *args, **options):
        task_name = options['task_name']
        task_args = options.get('args', [])
        job_id = str(uuid.uuid4())

        async_task(f'core.tasks.{task_name}', *task_args, task_name=task_name, job_id=job_id)
        self.stdout.write(self.style.SUCCESS(f'Job queued with ID: {job_id}'))