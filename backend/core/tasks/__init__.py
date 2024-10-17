from ..task_registry import TaskRegistry
from .hello_world import hello_world_task
from .parameterized_tasks import parameterized_task
from .update_sports import UpdateSportsTask
from .update_events import UpdateEventsTask
from .get_sports import GetSportsTask
from .get_events import GetEventsTask
from .get_odds_snapshot import GetOddsSnapshotTask
from loguru import logger

# Register tasks
TaskRegistry.register('hello_world_task', hello_world_task)
TaskRegistry.register('parameterized_task', parameterized_task)
TaskRegistry.register('update_sports_task', UpdateSportsTask.run)
TaskRegistry.register('update_events_task', UpdateEventsTask.run)
TaskRegistry.register('get_sports_task', GetSportsTask.run)
TaskRegistry.register('get_events_task', GetEventsTask.run)
TaskRegistry.register('get_odds_snapshot_task', GetOddsSnapshotTask.run)

# For debugging
logger.debug("Registered tasks:", TaskRegistry._tasks.keys())