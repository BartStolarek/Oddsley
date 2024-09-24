import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Runs autoflake, isort, and yapf formatters over the project'

    def handle(self, *args, **options):
        project_root = settings.BASE_DIR
        python_files = f"{project_root}/**/*.py"

        autoflake_cmd = f"autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place {python_files}"
        isort_cmd = f"isort {python_files}"
        yapf_cmd = f"yapf -r -i {python_files}"

        commands = [
            ('Autoflake', autoflake_cmd),
            ('isort', isort_cmd),
            ('yapf', yapf_cmd),
        ]

        for name, cmd in commands:
            self.stdout.write(f'Running {name}...')
            try:
                subprocess.run(cmd, shell=True, check=True, text=True)
                self.stdout.write(self.style.SUCCESS(f'{name} completed successfully'))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f'{name} failed: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('All formatting completed'))