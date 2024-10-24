from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.sport_service import SportService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger

class UpdateSportsTask(BaseTask):
    """ A task to fetch and update sports data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing UpdateSportsTask...")
        api_service = OddsAPIService(base_url=settings.THE_ODDS_API_BASE_URL, api_key=settings.THE_ODDS_API_KEY)
        sport_service = SportService()

        try:
            sports_data = api_service.get_sports(kwargs)
            updated_count = sport_service.upsert_sports(sports_data)
            return f"OddsAPI returned {len(sports_data)} sports, and successfully upserted {updated_count} into database."
        except Exception as e:
            logger.info(f"Error updating sports: {str(e)}")
            return "Error updating sports"

