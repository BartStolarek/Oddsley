from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'List all scheduled tasks'

    def handle(self, *args, **options):
        scheduled_tasks = Schedule.objects.all()

        if not scheduled_tasks:
            self.stdout.write(self.style.WARNING('No scheduled tasks found.'))
            return

        self.stdout.write(self.style.SUCCESS('Scheduled tasks:'))
        for task in scheduled_tasks:
            task_id = task.name.split('_')[-1]
            self.stdout.write(f'ID: {task_id}, Name: {task.func}, Schedule: {task.schedule_type}, Next run: {task.next_run}')
