# tests/test_management_commands.py

from django.core.management import call_command
from django.test import TestCase
from django.conf import settings
from io import StringIO
from unittest.mock import patch, MagicMock
import subprocess
from django_q.models import OrmQ, Schedule
from core.task_registry import TaskRegistry
import uuid

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
    @patch('subprocess.run')
    def test_format_command_uses_correct_paths(self, mock_subprocess_run):
        call_command('format')
        
        expected_path = '/test/project/root/**/*.py'
        
        # Check if each formatter command uses the correct path
        mock_subprocess_run.assert_any_call(f'autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place {expected_path}', shell=True, check=True, text=True)
        mock_subprocess_run.assert_any_call(f'isort {expected_path}', shell=True, check=True, text=True)
        mock_subprocess_run.assert_any_call(f'yapf -r -i {expected_path}', shell=True, check=True, text=True)

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


class JobCancelAllCommandTestCase(TestCase):
    @patch('core.management.commands.job_cancel_all.OrmQ.objects')
    def test_job_cancel_all_command(self, mock_orm_q):
        # Setup mock
        mock_orm_q.all.return_value.count.return_value = 5
        
        # Capture command output
        out = StringIO()
        call_command('job_cancel_all', stdout=out)

        # Check if OrmQ.objects.all().delete() was called
        mock_orm_q.all.return_value.delete.assert_called_once()

        # Check if the success message was printed
        self.assertIn('Cancelled 5 jobs.', out.getvalue())

class JobCancelCommandTestCase(TestCase):
    @patch('core.management.commands.job_cancel.OrmQ.objects')
    def test_job_cancel_command_success(self, mock_orm_q):
        # Setup mock
        mock_job = MagicMock()
        mock_orm_q.get.return_value = mock_job
        
        # Capture command output
        out = StringIO()
        call_command('job_cancel', 'test_job_id', stdout=out)

        # Check if OrmQ.objects.get() was called with correct ID
        mock_orm_q.get.assert_called_once_with(id='test_job_id')

        # Check if job.delete() was called
        mock_job.delete.assert_called_once()

        # Check if the success message was printed
        self.assertIn('Job test_job_id cancelled successfully.', out.getvalue())

    @patch('core.management.commands.job_cancel.OrmQ.objects')
    def test_job_cancel_command_not_found(self, mock_orm_q):
        # Setup mock to raise DoesNotExist
        mock_orm_q.get.side_effect = OrmQ.DoesNotExist
        
        # Capture command output
        out = StringIO()
        call_command('job_cancel', 'non_existent_id', stdout=out)

        # Check if the error message was printed
        self.assertIn('No job found with ID: non_existent_id', out.getvalue())

class JobListCommandTestCase(TestCase):
    @patch('core.management.commands.job_list.OrmQ.objects')
    def test_job_list_command_with_jobs(self, mock_orm_q):
        # Setup mock
        mock_jobs = [
            MagicMock(id='job1', func='task1'),
            MagicMock(id='job2', func='task2'),
        ]
        mock_orm_q.all.return_value = mock_jobs
        
        # Capture command output
        out = StringIO()
        call_command('job_list', stdout=out)

        # Check if the job details were printed
        output = out.getvalue()
        self.assertIn('Job ID: job1, Task: task1', output)
        self.assertIn('Job ID: job2, Task: task2', output)

    @patch('core.management.commands.job_list.OrmQ.objects')
    def test_job_list_command_no_jobs(self, mock_orm_q):
        # Setup mock to return empty list
        mock_orm_q.all.return_value = []
        
        # Capture command output
        out = StringIO()
        call_command('job_list', stdout=out)

        # Check if the warning message was printed
        self.assertIn('No jobs in the queue.', out.getvalue())


class ScheduleCancelAllCommandTestCase(TestCase):
    @patch('core.management.commands.schedule_cancel_all.Schedule.objects')
    def test_schedule_cancel_all_with_tasks(self, mock_schedule):
        # Setup mock
        mock_schedule.all.return_value.count.return_value = 2
        
        # Capture command output
        out = StringIO()
        call_command('schedule_cancel_all', stdout=out)

        # Check if Schedule.objects.all().delete() was called
        mock_schedule.all.return_value.delete.assert_called_once()

        # Check if the success message was printed
        self.assertIn('Successfully cancelled all 2 scheduled tasks.', out.getvalue())

    @patch('core.management.commands.schedule_cancel_all.Schedule.objects')
    def test_schedule_cancel_all_no_tasks(self, mock_schedule):
        # Setup mock
        mock_schedule.all.return_value.count.return_value = 0
        
        # Capture command output
        out = StringIO()
        call_command('schedule_cancel_all', stdout=out)

        # Check if the warning message was printed
        self.assertIn('No scheduled tasks found.', out.getvalue())

class ScheduleCancelCommandTestCase(TestCase):
    @patch('core.management.commands.schedule_cancel.Schedule.objects.get')
    def test_schedule_cancel_success(self, mock_get):
        # Setup mock
        mock_schedule = MagicMock()
        mock_schedule.func = 'core.tasks.test_task'
        mock_get.return_value = mock_schedule
        
        # Capture command output
        out = StringIO()
        call_command('schedule_cancel', 'test_id', stdout=out)

        # Check if Schedule.objects.get() was called with correct ID
        mock_get.assert_called_once_with(name__endswith='_test_id')

        # Check if schedule.delete() was called
        mock_schedule.delete.assert_called_once()

        # Check if the success message was printed
        self.assertIn('Successfully cancelled the scheduled task: test_task (ID: test_id)', out.getvalue())

    @patch('core.management.commands.schedule_cancel.Schedule.objects.get')
    def test_schedule_cancel_not_found(self, mock_get):
        # Setup mock to raise DoesNotExist
        mock_get.side_effect = Schedule.DoesNotExist
        
        # Capture command output
        out = StringIO()
        call_command('schedule_cancel', 'non_existent_id', stdout=out)

        # Check if the error message was printed
        self.assertIn('No scheduled task found with the ID: non_existent_id', out.getvalue())

class ScheduleListCommandTestCase(TestCase):
    @patch('core.management.commands.schedule_list.Schedule.objects')
    def test_schedule_list_with_tasks(self, mock_schedule):
        mock_tasks = [
            MagicMock(name='task1_schedule_id1', func='core.tasks.task1', schedule_type='HOURLY', next_run='2023-01-01 00:00:00'),
            MagicMock(name='task2_schedule_id2', func='core.tasks.task2', schedule_type='DAILY', next_run='2023-01-02 00:00:00'),
        ]
        mock_schedule.all.return_value = mock_tasks
        out = StringIO()
        call_command('schedule_list', stdout=out)
        output = out.getvalue()
        self.assertIn('Name: core.tasks.task1, Schedule: HOURLY, Next run: 2023-01-01 00:00:00', output)
        self.assertIn('Name: core.tasks.task2, Schedule: DAILY, Next run: 2023-01-02 00:00:00', output)

class ScheduleTaskCommandTestCase(TestCase):
    @patch('core.management.commands.schedule_task.schedule')
    @patch('core.management.commands.schedule_task.TaskRegistry.get_task')
    @patch('core.management.commands.schedule_task.uuid.uuid4')
    @patch('core.management.commands.schedule_task.Schedule')
    def test_schedule_task_success(self, mock_schedule_model, mock_uuid, mock_get_task, mock_schedule):
        mock_uuid.return_value = 'test-uuid'
        mock_get_task.return_value = MagicMock()
        mock_schedule_model.DAILY = Schedule.DAILY
        mock_schedule_model.next_time = MagicMock(return_value='2023-01-01 12:00:00')
        out = StringIO()
        call_command('schedule_task', 'test_task', schedule_type='DAILY', hour='12', minute='0', stdout=out)
        mock_schedule.assert_called_once()
        self.assertIn('Task test_task scheduled successfully with ID: test-uuid', out.getvalue())
