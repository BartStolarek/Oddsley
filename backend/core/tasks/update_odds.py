from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.odd_service import OddService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger
from datetime import datetime


class UpdateOddsTask(BaseTask):
    """ A task to fetch and update odds data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @staticmethod
    def check_required_parameters(kwargs) -> None:
        required_params = [
            ('sport', str),
            ('regions', list),
            ('markets', list),
            ('date', datetime)
        ]
        
        for param, param_type in required_params:
            if not kwargs.get(param):
                logger.error(f"Task is missing required param '{param}' (keyword argument), e.g. 'python manage.py task_run <your_task> -kw sport=americanfootball_nfl'. ")
                raise ValueError("Insufficient arguments provided to task")
            
            # Replace kwargs with the correct type
            if param_type == datetime:
                try:
                    kwargs[param] = datetime.strptime(kwargs[param], "%Y-%m-%d/%H:%M:%S")
                except ValueError:
                    logger.error(f"Date value provided is not in the correct format, should be 'YYYY-MM-DD/HH:MM:SS', e.g. '2021-09-01/00:00:00' what was provided was '{kwargs[param]}'")
                    raise ValueError("Incorrect date format provided")
                    
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing UpdateOddsTask...")
        api_service = OddsAPIService(base_url=settings.THE_ODDS_API_BASE_URL, api_key=settings.THE_ODDS_API_KEY)
        odd_service = OddService()

        try:
            
            cls.check_required_parameters(kwargs)
            
            odds_data = api_service.get_historical_odds(**kwargs)
            upserted_count = odd_service.upsert_odds(odds_data)
            return f"OddsAPI returned {len(odds_data['data'])} odds, and successfully upserted {upserted_count} into database."
        except Exception as e:
            logger.error(f"Error updating sports: {str(e)}")
            return "Error updating sports"

