from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Cancel a scheduled task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=str, help='ID of the task to cancel')

    def handle(self, *args, **options):
        task_id = options['task_id']

        try:
            schedule = Schedule.objects.get(name__endswith=f'_{task_id}')
            task_name = schedule.func.split('.')[-1]
            schedule.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully cancelled the scheduled task: {task_name} (ID: {task_id})'))
        except Schedule.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No scheduled task found with the ID: {task_id}'))