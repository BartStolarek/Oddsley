from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.oddsnapshot_service import OddSnapshotService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger


class GetOddsSnapshotTask(BaseTask):
    """ A task to fetch and update oddssnapshot data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing UpdateoddssnapshotTask...")
        api_service = OddsAPIService(base_url=settings.THE_ODDS_API_BASE_URL, api_key=settings.THE_ODDS_API_KEY)
        oddsnapshot_service = OddSnapshotService()

        try:
            
            if kwargs.get('sport'):
                sport = kwargs['sport']
            else:
                logger.error("Task requires a 'sport' keyword argument, e.g. 'sport=americanfootball_nfl'. Call 'get_sports_task' to get a list of available sports. Example of calling command correctly 'python manage.py task_run update_events_task -kw sport=americanfootball_nfl'")
                raise ValueError("Insufficient arguments provided to task")
            
            if kwargs.get('regions'):
                regions = kwargs['regions']
            else:
                logger.error("Task requires a 'regions' keyword argument, e.g. 'regions=us'. Call 'get_sports_task' to get a list of available sports. Example of calling command correctly 'python manage.py task_run update_events_task -kw sport=americanfootball_nfl'")
                raise ValueError("Insufficient arguments provided to task")
            
            odds_snapshot = api_service.get_odds(sport=sport, regions=regions, kwargs=kwargs)
            updated_count = oddsnapshot_service.upsert_oddssnapshot(odds_snapshot)
            return f"OddsAPI returned {len(odds_snapshot)} oddssnapshot, and successfully upserted {updated_count} into database."
        except Exception as e:
            logger.error(f"Error updating odds snapshot: {str(e)}")
            return "Error updating odds snapshot"

