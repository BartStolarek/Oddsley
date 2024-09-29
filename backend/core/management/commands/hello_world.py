from django.core.management.base import BaseCommand
from core.tasks.hello_world import hello_world_task

class Command(BaseCommand):
    help = 'Runs a hello world job'

    def handle(self, *args, **options):
        # Run the hello world task not asynchonously
        hello_world_task()
        
        
