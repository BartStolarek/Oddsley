import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Runs autoflake, isort, and yapf formatters over the project'

    def handle(self, *args, **options):
        project_root = settings.BASE_DIR

        # Directories and patterns to exclude
        exclude_dirs = [
            'venv',
            '.venv',
            'env',
            '.env',
            'node_modules',
            'migrations',
            '__pycache__',
            '.git',
            'static',
            'media',
            'build',
            'dist',
        ]

        exclude_files = [
            'settings.py',
            'manage.py',
        ]

        # Generate the list of Python files, excluding specified directories and files
        python_files = []
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith('.py') and file not in exclude_files:
                    python_files.append(os.path.join(root, file))

        python_files_str = ' '.join(python_files)

        self.stdout.write(f"Project Root dir: {project_root}")
        self.stdout.write(f"Number of files to format: {len(python_files)}")

        autoflake_cmd = f"autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place {python_files_str}"
        isort_cmd = f"isort {python_files_str}"
        yapf_cmd = f"yapf -r -i {python_files_str}"

        commands = [
            ('Autoflake', autoflake_cmd),
            ('isort', isort_cmd),
            ('yapf', yapf_cmd),
        ]

        for name, cmd in commands:
            self.stdout.write(f'Running {name}...')
            try:
                subprocess.run(cmd, shell=True, check=True, text=True)
                self.stdout.write(
                    self.style.SUCCESS(f'{name} completed successfully'))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f'{name} failed: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('All formatting completed'))

    def print_files(self, files):
        for file in files:
            self.stdout.write(file)
