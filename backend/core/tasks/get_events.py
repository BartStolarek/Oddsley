from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.event_service import EventService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger

class GetEventsTask(BaseTask):
    """ A task to get events data from the database

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing GetEventsTask...")
        event_service = EventService()

        try:
            return event_service.get_events(**kwargs)
        except Exception as e:
            logger.info(f"Error getting events: {str(e)}")
            return "Error getting events"

