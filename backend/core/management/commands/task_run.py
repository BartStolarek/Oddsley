from django.core.management.base import BaseCommand
from core.task_registry import TaskRegistry
from loguru import logger
import ast
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from io import StringIO
import sys

class Command(BaseCommand):
    """ A command to run a specified task immediately or repeatedly within a date range

    Args:
        BaseCommand (Django BaseCommand Parent Class): The base class from which all management commands ultimately derive.
    """
    help = 'Run a specified task immediately or repeatedly within a date range'

    def add_arguments(self, parser) -> None:
        """ Add arguments to the command

        Args:
            parser (ArgumentParser): The parser object to which arguments should be added
        """
        parser.add_argument('task_name', type=str, help='Name of the task to run')
        parser.add_argument('-kw', '--kwargs', nargs='+', help='Optional keyword arguments for the task')
        parser.add_argument('--start', type=str, help='Start date and time (format: YYYY-MM-DD/HH:MM:SS)')
        parser.add_argument('--end', type=str, help='End date and time (format: YYYY-MM-DD/HH:MM:SS)')
        parser.add_argument('--interval_value', type=str, help='Interval value (e.g., "5")')
        parser.add_argument('--interval_unit', type=str, help='Interval unit (e.g., "min", "hour", "day", "week")')

    def handle(self, *args, **options):
        """ Handle the command by checking the task name, and parsing the keyword arguments
        """
        task_name = options['task_name']
        kwargs = self.parse_kwargs(options.get('kwargs', []))
        start = options.get('start')
        end = options.get('end')
        interval_value = options.get('interval_value')
        interval_unit = options.get('interval_unit')

        logger.debug(f"Available tasks: {list(TaskRegistry._tasks.keys())}")

        if all([start, end, interval_value, interval_unit]):
            self.run_task_with_interval(task_name, kwargs, start, end, interval_value, interval_unit)
        else:
            self.run_single_task(task_name, kwargs)

    def run_task_with_interval(self, task_name, kwargs, start, end, interval_value, interval_unit):
        start_time = datetime.strptime(start, '%Y-%m-%d/%H:%M:%S')
        end_time = datetime.strptime(end, '%Y-%m-%d/%H:%M:%S')
        interval_value = int(interval_value)

        total_iterations = self.calculate_total_iterations(start_time, end_time, interval_value, interval_unit)

        with tqdm(total=total_iterations, desc="Progress", unit="iteration") as pbar:
            current_time = start_time
            while current_time <= end_time:
                # Capture the output of the task
                captured_output = StringIO()
                sys.stdout = captured_output
                sys.stderr = captured_output

                kwargs['date'] = current_time.strftime('%Y-%m-%d/%H:%M:%S')
                self.run_single_task(task_name, kwargs)

                # Restore standard output and error
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

                # Update progress bar description with current time
                pbar.set_description(f"Running task for date: {current_time}")

                # Display captured output
                task_output = captured_output.getvalue().strip()
                if task_output:
                    tqdm.write(task_output)

                if interval_unit.startswith('minute'):
                    current_time += timedelta(minutes=interval_value)
                elif interval_unit.startswith('hour'):
                    current_time += timedelta(hours=interval_value)
                elif interval_unit.startswith('day'):
                    current_time += timedelta(days=interval_value)
                elif interval_unit.startswith('week'):
                    current_time += timedelta(weeks=interval_value)
                else:
                    logger.error(f"Invalid interval unit: {interval_unit}")
                    break

                pbar.update(1)

    def calculate_total_iterations(self, start_time, end_time, interval_value, interval_unit):
        if interval_unit.startswith('minute'):
            total_minutes = (end_time - start_time).total_seconds() / 60
            return int(total_minutes / interval_value) + 1
        elif interval_unit.startswith('hour'):
            total_hours = (end_time - start_time).total_seconds() / 3600
            return int(total_hours / interval_value) + 1
        elif interval_unit.startswith('day'):
            total_days = (end_time - start_time).days
            return int(total_days / interval_value) + 1
        elif interval_unit.startswith('week'):
            total_weeks = (end_time - start_time).days / 7
            return int(total_weeks / interval_value) + 1
        else:
            raise ValueError(f"Invalid interval unit: {interval_unit}")

    def run_single_task(self, task_name, kwargs):
        try:
            result = TaskRegistry.run_task(task_name, **kwargs)
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
            return kwargs
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
            if ',' in value:
                return value.split(',')
            # If it's not a valid Python literal, return it as a string
            return value