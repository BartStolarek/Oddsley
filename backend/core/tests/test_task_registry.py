# In backend/core/tests/test_task_registry.py

from django.test import TestCase

from core.task_registry import TaskRegistry


def mock_task():
    return "This is a mock task."


class TaskRegistryTests(TestCase):

    def setUp(self):
        TaskRegistry._tasks.clear()  # Clear the registry before each test

    def test_register_task(self):
        TaskRegistry.register('mock_task', mock_task)
        self.assertIn('mock_task', TaskRegistry._tasks)
        self.assertEqual(TaskRegistry._tasks['mock_task'](),
                         "This is a mock task.")

    def test_get_registered_task(self):
        TaskRegistry.register('mock_task', mock_task)
        task = TaskRegistry.get_task('mock_task')
        self.assertEqual(task(), "This is a mock task.")

    def test_get_unregistered_task(self):
        with self.assertRaises(ValueError) as context:
            TaskRegistry.get_task('non_existent_task')
        self.assertEqual(
            str(context.exception),
            "Task non_existent_task not found in registry or as importable string"
        )

    def test_get_importable_task(self):
        # Assuming you have a task defined in a module that can be imported
        TaskRegistry.register('backend.core.tests.mock_task', mock_task)
        task = TaskRegistry.get_task('backend.core.tests.mock_task')
        self.assertEqual(task(), "This is a mock task.")

    def test_import_error(self):
        with self.assertRaises(ValueError) as context:
            TaskRegistry.get_task('some_non_existent_module.some_function')
        self.assertEqual(
            str(context.exception),
            "Task some_non_existent_module.some_function not found in registry or as importable string"
        )
