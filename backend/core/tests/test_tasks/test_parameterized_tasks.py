# In backend/core/tests/test_task_registry.py

from django.test import TestCase

from core.task_registry import TaskRegistry
from core.tasks.hello_world import hello_world_task
from core.tasks.parameterized_tasks import parameterized_task


class TaskRegistryTests(TestCase):

    def setUp(self):
        TaskRegistry._tasks.clear()  # Clear tasks before each test

    def test_register_task(self):
        TaskRegistry.register("hello_world", hello_world_task)
        self.assertIn("hello_world", TaskRegistry._tasks)

    def test_get_registered_task(self):
        TaskRegistry.register("hello_world", hello_world_task)
        task = TaskRegistry.get_task("hello_world")
        self.assertIsNotNone(task)

    def test_execute_hello_world_task(self):
        TaskRegistry.register("hello_world", hello_world_task)
        task = TaskRegistry.get_task("hello_world")
        # Redirect stdout to capture print output
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        task()  # Execute the task

        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(captured_output.getvalue().strip(),
                         "Hello World task executed")

    def test_register_parameterized_task(self):
        TaskRegistry.register("parameterized_task", parameterized_task)
        self.assertIn("parameterized_task", TaskRegistry._tasks)

    def test_execute_parameterized_task(self):
        TaskRegistry.register("parameterized_task", parameterized_task)
        task = TaskRegistry.get_task("parameterized_task")

        # Redirect stdout to capture print output
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        task("value1", "value2")  # Execute the parameterized task

        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(captured_output.getvalue().strip(),
                         "Parameterized task executed with value1 and value2")

    def test_get_unregistered_task(self):
        with self.assertRaises(ValueError) as context:
            TaskRegistry.get_task("non_existent_task")

        self.assertEqual(
            str(context.exception),
            "Task non_existent_task not found in registry or as importable string"
        )
