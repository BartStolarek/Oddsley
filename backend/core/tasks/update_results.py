from django.conf import settings
from core.services.result_service import ResultService
from core.task_registry import TaskRegistry
from .base_task import BaseTask
from loguru import logger
from datetime import datetime


class UpdateResultsTask(BaseTask):
    """ A task to fetch and update results data from the Odds API

    Args:
        BaseTask (Class): BaseTask class that has some common methods and actions for all tasks

    """
    
    @staticmethod
    def check_paramaters(kwargs) -> None:
        required_params = [
            ('sport', str),
            ('csv', str),
            ('tz', str)
        ]
        
        for param, param_type in required_params:
            if not kwargs.get(param):
                logger.error(f"Task is missing required param '{param}' (keyword argument), e.g. 'python manage.py task_run <your_task> -kw sport=americanfootball_nfl'. ")
                raise ValueError("Insufficient arguments provided to task")
            
            if not isinstance(param, param_type):
                logger.error(f"Incorrect param type provided for '{param}', got '{type(param)}' expected '{param_type}'")
                raise ValueError("Incorrect argument type provided")
    
    @classmethod
    def execute(cls, **kwargs) -> str:
        """ Execute the task

        Returns:
            str: A message indicating the result of the task
        """
        logger.info("Executing UpdateResultsTask...")
        result_service = ResultService()

        try:
            
            cls.check_paramaters(kwargs)
            
            results_data = result_service.read_csv(kwargs.get('csv'))
            
            logger.debug(f"Loaded {len(results_data)} results from CSV")
            
            results_data = result_service.match_results_to_events(results_data, sport=kwargs.get('sport'), source_timezone=kwargs.get('tz'))

            #updated_count = result_service.upsert_results(results_data)
            
            #return f"Loaded {len(results_data)} event results, and successfully upserted {updated_count} into database."
            exit()
        except Exception as e:
            logger.error(f"Error updating results: {str(e)}")
            return "Error updating results"

