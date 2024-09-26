# In backend/core/tasks.py

from .task_registry import TaskRegistry


def hello_world_task():
    print("Hello World task executed")


def parameterized_task(param1, param2):
    print(f"Parameterized task executed with {param1} and {param2}")


# Register tasks
TaskRegistry.register('hello_world_task', hello_world_task)
TaskRegistry.register('parameterized_task', parameterized_task)