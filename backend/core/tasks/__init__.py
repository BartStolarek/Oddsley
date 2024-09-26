from ..task_registry import TaskRegistry
from .hello_world import hello_world_task
from .parameterized_tasks import parameterized_task

# Register tasks
TaskRegistry.register('hello_world_task', hello_world_task)
TaskRegistry.register('parameterized_task', parameterized_task)
