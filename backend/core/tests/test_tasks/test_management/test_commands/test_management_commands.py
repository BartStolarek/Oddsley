# tests/test_management_commands.py

import subprocess
from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase
import os


class FormatCommandTestCase(TestCase):

    @patch('subprocess.run')
    def test_format_command_success(self, mock_subprocess_run):
        # Mock successful subprocess runs
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        # Capture command output
        out = StringIO()
        call_command('format', stdout=out)

        output = out.getvalue()

        # Check if all three formatters were called
        self.assertEqual(mock_subprocess_run.call_count, 3)

        # Check if success messages were printed
        self.assertIn('Running Autoflake...', output)
        self.assertIn('Autoflake completed successfully', output)
        self.assertIn('Running isort...', output)
        self.assertIn('isort completed successfully', output)
        self.assertIn('Running yapf...', output)
        self.assertIn('yapf completed successfully', output)
        self.assertIn('All formatting completed', output)

    @patch('subprocess.run')
    def test_format_command_failure(self, mock_subprocess_run):
        # Mock a failed subprocess run for the second formatter (isort)
        def side_effect(*args, **kwargs):
            if 'isort' in args[0]:
                raise subprocess.CalledProcessError(1, 'isort')
            return MagicMock(returncode=0)

        mock_subprocess_run.side_effect = side_effect

        # Capture command output
        out = StringIO()
        err = StringIO()
        call_command('format', stdout=out, stderr=err)

        output = out.getvalue()
        error_output = err.getvalue()

        # Check if all three formatters were attempted
        self.assertEqual(mock_subprocess_run.call_count, 3)

        # Check if success and error messages were printed appropriately
        self.assertIn('Running Autoflake...', output)
        self.assertIn('Autoflake completed successfully', output)
        self.assertIn('Running isort...', output)
        self.assertIn('isort failed:', error_output)
        self.assertIn('Running yapf...', output)
        self.assertIn('yapf completed successfully', output)
        self.assertIn('All formatting completed', output)

    @patch('django.conf.settings.BASE_DIR', new='/test/project/root')
    @patch('os.walk')
    @patch('subprocess.run')
    def test_format_command_uses_correct_paths(self, mock_subprocess_run, mock_os_walk):
        # Mock os.walk to return some test files
        mock_os_walk.return_value = [
            ('/test/project/root', [], ['file1.py', 'file2.py']),
            ('/test/project/root/subdir', [], ['file3.py']),
        ]

        call_command('format')

        expected_files = ' '.join([
            '/test/project/root/file1.py',
            '/test/project/root/file2.py',
            '/test/project/root/subdir/file3.py'
        ])

        # Check if each formatter command uses the correct files
        mock_subprocess_run.assert_any_call(
            f'autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place {expected_files}',
            shell=True,
            check=True,
            text=True)
        mock_subprocess_run.assert_any_call(f'isort {expected_files}',
                                            shell=True,
                                            check=True,
                                            text=True)
        mock_subprocess_run.assert_any_call(f'yapf -r -i {expected_files}',
                                            shell=True,
                                            check=True,
                                            text=True)

class HelloWorldCommandTestCase(TestCase):

    @patch('core.management.commands.hello_world.async_task')
    def test_hello_world_command(self, mock_async_task):
        # Capture command output
        out = StringIO()
        call_command('hello_world', stdout=out)

        # Check if async_task was called with the correct arguments
        mock_async_task.assert_called_once_with('core.tasks.hello_world_task')

        # Check if the success message was printed
        self.assertIn('Hello World job queued successfully', out.getvalue())
