from django.conf import settings
from core.services.oddsapi_service import OddsAPIService
from core.services.event_service import EventService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger
from datetime import datetime


class UpdateEventsTask(BaseTask):
    """ A task to fetch and update events data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @staticmethod
    def check_paramaters(kwargs) -> None:
        required_params = [
            ('sport', str)
        ]
        
        for param, param_type in required_params:
            if not kwargs.get(param):
                logger.error(f"Task is missing required param '{param}' (keyword argument), e.g. 'python manage.py task_run <your_task> -kw sport=americanfootball_nfl'. ")
                raise ValueError("Insufficient arguments provided to task")
            
            if not isinstance(param, param_type):
                logger.error(f"Incorrect param type provided for '{param}', got '{type(param)}' expected '{param_type}'")
                raise ValueError("Incorrect argument type provided")

        optional_params = [
            ('date', datetime) # Historical events
        ]
        
        for param, param_type in optional_params:
            if kwargs.get(param):
                if param_type == datetime:
                    try:
                        kwargs[param] = datetime.strptime(kwargs[param], "%Y-%m-%d/%H:%M:%S")
                    except ValueError:
                        logger.error(f"Date value provided is not in the correct format, should be 'YYYY-MM-DD/HH:MM:SS', e.g. '2021-09-01/00:00:00' what was provided was '{kwargs[param]}'")
                        raise ValueError("Incorrect date format provided")
                elif not isinstance(param, param_type):
                    logger.error(f"Incorrect param type provided for '{param}', got '{type(param)}' expected '{param_type}'")
                    raise ValueError("Incorrect argument type provided")
    
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
            
            cls.check_paramaters(kwargs)
            
            events_data = api_service.get_historical_events(**kwargs) if kwargs.get('date') else api_service.get_events(**kwargs)

            updated_count = event_service.upsert_events(events_data['data']) if kwargs.get('date') else event_service.upsert_events(events_data)
            
            odds_api_len = len(events_data['data']) if kwargs.get('date') else len(events_data)
            
            return f"OddsAPI returned {odds_api_len} events, and successfully upserted {updated_count} into database."
        except Exception as e:
            logger.error(f"Error updating events: {str(e)}")
            return "Error updating events"

