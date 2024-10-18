from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.event_service import EventService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger


class UpdateEventsTask(BaseTask):
    """ A task to fetch and update events data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing UpdateEventsTask...")
        api_service = OddsAPIService(base_url=settings.THE_ODDS_API_BASE_URL, api_key=settings.THE_ODDS_API_KEY)
        event_service = EventService()

        try:
            
            if kwargs.get('sport'):
                sport = kwargs['sport']
            else:
                logger.error("Task requires a 'sport' keyword argument, e.g. 'sport=americanfootball_nfl'. Call 'get_sports_task' to get a list of available sports. Example of calling command correctly 'python manage.py task_run update_events_task -kw sport=americanfootball_nfl'")
                raise ValueError("Insufficient arguments provided to task")
            
            events_data = api_service.get_events(sport=sport, kwargs=kwargs)
            updated_count = event_service.upsert_events(events_data)
            return f"OddsAPI returned {len(events_data)} events, and successfully upserted {updated_count} into database."
        except Exception as e:
            logger.error(f"Error updating sports: {str(e)}")
            return "Error updating sports"

