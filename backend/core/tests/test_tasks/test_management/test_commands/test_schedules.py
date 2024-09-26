from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase
from django_q.models import Schedule


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
        self.assertIn('Successfully cancelled all 2 scheduled tasks.',
                      out.getvalue())

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
        self.assertIn(
            'Successfully cancelled the scheduled task: test_task (ID: test_id)',
            out.getvalue())

    @patch('core.management.commands.schedule_cancel.Schedule.objects.get')
    def test_schedule_cancel_not_found(self, mock_get):
        # Setup mock to raise DoesNotExist
        mock_get.side_effect = Schedule.DoesNotExist

        # Capture command output
        out = StringIO()
        call_command('schedule_cancel', 'non_existent_id', stdout=out)

        # Check if the error message was printed
        self.assertIn('No scheduled task found with the ID: non_existent_id',
                      out.getvalue())


class ScheduleListCommandTestCase(TestCase):

    @patch('core.management.commands.schedule_list.Schedule.objects')
    def test_schedule_list_with_tasks(self, mock_schedule):
        mock_tasks = [
            MagicMock(name='task1_schedule_id1',
                      func='core.tasks.task1',
                      schedule_type='HOURLY',
                      next_run='2023-01-01 00:00:00'),
            MagicMock(name='task2_schedule_id2',
                      func='core.tasks.task2',
                      schedule_type='DAILY',
                      next_run='2023-01-02 00:00:00'),
        ]
        mock_schedule.all.return_value = mock_tasks
        out = StringIO()
        call_command('schedule_list', stdout=out)
        output = out.getvalue()
        self.assertIn(
            'Name: core.tasks.task1, Schedule: HOURLY, Next run: 2023-01-01 00:00:00',
            output)
        self.assertIn(
            'Name: core.tasks.task2, Schedule: DAILY, Next run: 2023-01-02 00:00:00',
            output)


class ScheduleTaskCommandTestCase(TestCase):

    @patch('core.management.commands.schedule_task.schedule')
    @patch('core.management.commands.schedule_task.TaskRegistry.get_task')
    @patch('core.management.commands.schedule_task.uuid.uuid4')
    @patch('core.management.commands.schedule_task.Schedule')
    def test_schedule_task_success(self, mock_schedule_model, mock_uuid,
                                   mock_get_task, mock_schedule):
        mock_uuid.return_value = 'test-uuid'
        mock_get_task.return_value = MagicMock()
        mock_schedule_model.DAILY = Schedule.DAILY
        mock_schedule_model.next_time = MagicMock(
            return_value='2023-01-01 12:00:00')
        out = StringIO()
        call_command('schedule_task',
                     'test_task',
                     schedule_type='DAILY',
                     hour='12',
                     minute='0',
                     stdout=out)
        mock_schedule.assert_called_once()
        self.assertIn(
            'Task test_task scheduled successfully with ID: test-uuid',
            out.getvalue())
