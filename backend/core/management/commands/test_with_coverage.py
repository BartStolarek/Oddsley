from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import coverage
from django.test.utils import get_runner

class Command(BaseCommand):
    help = 'Runs tests with coverage.'

    def handle(self, *args, **options):
        cov = coverage.Coverage()
        cov.start()

        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(['tests'])  # replace "core" with your app name

        cov.stop()
        cov.save()

        cov.report()
        cov.html_report(directory='htmlcov')

        sys.exit(bool(failures))