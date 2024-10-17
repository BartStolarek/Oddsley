from django.core.management.base import BaseCommand
from core.task_registry import TaskRegistry
from loguru import logger
import ast
import pandas as pd

class Command(BaseCommand):
    """ A command to run a specified task immediately

    Args:
        BaseCommand (Django BaseCommand Parent Class): The base class from which all management commands ultimately derive.
    """
    help = 'Run a specified task immediately'

    def add_arguments(self, parser) -> None:
        """ Add arguments to the command

        Args:
            parser (ArgumentParser): The parser object to which arguments should be added
        """
        parser.add_argument('task_name', type=str, help='Name of the task to run')
        parser.add_argument('-kw', '--kwargs', nargs='+', help='Optional keyword arguments for the task')

    def handle(self, *args, **options):
        """ Handle the command by checking the task name, and parsing the keyword arguments
        """
        task_name = options['task_name']
        kwargs = self.parse_kwargs(options.get('kwargs', []))

        logger.debug(f"Available tasks: {list(TaskRegistry._tasks.keys())}")
        
        try:
            
            result = TaskRegistry.run_task(task_name, **kwargs) if kwargs else TaskRegistry.run_task(task_name)
            logger.success(f'Task {task_name} executed successfully.')
            if result:
                
                if isinstance(result, list) and isinstance(result[0], dict):
                    df = pd.DataFrame(result)
                    with pd.option_context('display.max_rows', None, 'display.width', None, 'display.max_columns', None, 'display.max_colwidth', None):
                        print(df)
                else:
                    logger.info(str(result))
                
        except Exception as e:
            logger.error(f'Error running task {task_name}: {str(e)}. Available tasks: {list(TaskRegistry._tasks.keys())}')

    def parse_kwargs(self, kwargs_list: list) -> dict:
        """ Parse the keyword arguments into a dictionary

        Args:
            kwargs_list (list): A list of keyword arguments in the form of 'key=value' provided on the command line

        Returns:
            dict: A dictionary of keyword arguments
        """
        kwargs = {}
        if not kwargs_list:
            return
        for kw in kwargs_list:
            try:
                key, value = kw.split('=', 1)
                kwargs[key] = self.parse_value(value)
            except ValueError:
                logger.warning(f"Ignoring malformed kwarg: {kw}")
        return kwargs

    def parse_value(self, value: str):
        """ Parse a value into a Python literal if possible

        Args:
            value (str): The value to parse

        Returns:
            Any: The parsed value, or the original value if it can't be parsed
        """
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            # If it's not a valid Python literal, return it as a string
            return value