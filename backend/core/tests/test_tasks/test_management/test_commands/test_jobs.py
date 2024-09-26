from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase
from django_q.models import OrmQ


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
        self.assertIn('Job test_job_id cancelled successfully.',
                      out.getvalue())

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
