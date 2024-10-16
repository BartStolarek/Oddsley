from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.sport_service import SportService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger

class GetSportsTask(BaseTask):
    """ A task to get sports data from the database

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing GetSportsTask...")
        sport_service = SportService()

        try:
            return sport_service.get_sports(**kwargs)
        except Exception as e:
            logger.info(f"Error getting sports: {str(e)}")
            return "Error getting sports"

