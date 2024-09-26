from django.core.management.base import BaseCommand
from django_q.tasks import async_task


class Command(BaseCommand):
    help = 'Runs a hello world job'

    def handle(self, *args, **options):
        async_task('core.tasks.hello_world_task')
        self.stdout.write(self.style.SUCCESS('Hello World job queued successfully'))
