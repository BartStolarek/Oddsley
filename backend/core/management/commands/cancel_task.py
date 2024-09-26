# In backend/core/management/commands/cancel_task.py

from django.core.management.base import BaseCommand
from django_q.models import Schedule

class Command(BaseCommand):
    help = 'Cancel a scheduled task'

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='Name of the task to cancel')

    def handle(self, *args, **options):
        task_name = options['task_name']
        schedule_name = f'{task_name}_schedule'

        try:
            schedule = Schedule.objects.get(name=schedule_name)
            schedule.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully cancelled the scheduled task: {task_name}'))
        except Schedule.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No scheduled task found with the name: {task_name}'))