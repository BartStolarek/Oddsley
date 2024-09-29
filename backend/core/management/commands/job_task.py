import uuid
from django.core.management.base import BaseCommand
from django_q.tasks import async_task
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Queue a job with a specified task'

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='Name of the task to queue')
        parser.add_argument('--args', nargs='*', default=[], help='Optional arguments for the task')

    def handle(self, *args, **options):
        task_name = options['task_name']
        task_args = options.get('args', [])
        job_id = str(uuid.uuid4())

        try:
            # Pass task_name and job_id as explicit arguments
            async_task(f'core.tasks.{task_name}.{task_name}_task', 
                       *task_args, 
                       task_name=task_name, 
                       job_id=job_id,
                       # Add these two lines:
                       _task_name=task_name,
                       _job_id=job_id)
            
            logger.info(f'Job queued with ID: {job_id} (Task: {task_name})')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error queuing job: {str(e)} (Task: {task_name})'))