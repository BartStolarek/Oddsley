from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from django_q.models import Schedule
from core.task_registry import TaskRegistry
import uuid


class Command(BaseCommand):
    help = 'Schedule a task with various timing options'

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='Name of the task to schedule')
        parser.add_argument('--schedule_type', type=str, choices=['MINUTES', 'HOURLY', 'DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY'], help='Type of schedule')
        parser.add_argument('--interval', type=int, help='Interval for MINUTES schedule type')
        parser.add_argument('--hour', type=int, help='Hour for DAILY, WEEKLY, MONTHLY schedules (0-23)')
        parser.add_argument('--minute', type=int, help='Minute for schedules with specific times (0-59)')
        parser.add_argument('--day_of_week', type=int, help='Day of week for WEEKLY schedule (0-6, where 0 is Monday)')
        parser.add_argument('--day_of_month', type=int, help='Day of month for MONTHLY schedule (1-31)')
        parser.add_argument('--params', nargs='*', help='Parameters to pass to the task')

    def handle(self, *args, **options):
        task_name = options['task_name']
        schedule_type = options['schedule_type']
        
        try:
            TaskRegistry.get_task(task_name)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        unique_id = str(uuid.uuid4())
        schedule_name = f'{task_name}_schedule_{unique_id}'

        schedule_kwargs = {
            'func': f'core.tasks.{task_name}',
            'name': schedule_name,
            'schedule_type': getattr(Schedule, schedule_type),
        }

        if schedule_type == 'MINUTES':
            schedule_kwargs['minutes'] = options['interval']
        elif schedule_type in ['DAILY', 'WEEKLY', 'MONTHLY']:
            schedule_kwargs['next_run'] = Schedule.next_time(
                hour=options.get('hour', 0),
                minute=options.get('minute', 0)
            )

        if schedule_type == 'WEEKLY':
            schedule_kwargs['day_of_week'] = options['day_of_week']
        elif schedule_type == 'MONTHLY':
            schedule_kwargs['day_of_month'] = options['day_of_month']

        if options['params']:
            schedule_kwargs['args'] = options['params']

        # Create the schedule
        schedule(**schedule_kwargs)

        self.stdout.write(self.style.SUCCESS(f'Task {task_name} scheduled successfully with ID: {unique_id}'))