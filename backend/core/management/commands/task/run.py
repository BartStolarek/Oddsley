from django.core.management.base import BaseCommand
from core.task_registry import TaskRegistry

class Command(BaseCommand):
    help = 'Run a specified task immediately'

    def add_arguments(self, parser):
        parser.add_argument('task_name', type=str, help='Name of the task to run')
        parser.add_argument('--args', nargs='*', help='Optional arguments for the task')

    def handle(self, *args, **options):
        task_name = options['task_name']
        task_args = options.get('args', [])

        try:
            task = TaskRegistry.get_task(task_name)
            result = task(*task_args)
            self.stdout.write(self.style.SUCCESS(f'Task {task_name} executed successfully.'))
            if result:
                self.stdout.write(str(result))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error running task {task_name}: {str(e)}'))