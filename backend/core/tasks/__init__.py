from ..task_registry import TaskRegistry
from .hello_world import hello_world_task
from .parameterized_tasks import parameterized_task
from .get_sports import GetSportsTask

# Register tasks
TaskRegistry.register('hello_world_task', hello_world_task)
TaskRegistry.register('parameterized_task', parameterized_task)
TaskRegistry.register('get_sports_task', GetSportsTask.run)

# For debugging
print("Registered tasks:", TaskRegistry._tasks.keys())