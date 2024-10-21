from django.db import transaction
from core.models import EventResult as Result
from loguru import logger
import pandas as pd
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from core.models import Event, Team
import pytz
from django.conf import settings


class ResultService:
    """ Service class to interact with the Result model
    """
    
    def __init__(self):
        logger.debug("resultservice initialized")
    
    def read_csv(self, csv_path: str) -> pd.DataFrame:
        """ Read results data from a CSV file

        Args:
            csv_path (str): Path to the CSV file

        Returns:
            list[dict]: List of results data
        """
        logger.debug(f"Reading results data from {csv_path}")
        try:
            full_path = f"{settings.BASE_DIR}/{csv_path}"
            results_data = pd.read_csv(full_path)
            return results_data
        except Exception as e:
            logger.error(f"Error reading results data: {str(e)}")
            raise
    
    
    
    @staticmethod
    def validate_results_data(results_data: pd.DataFrame) -> None:
        """ Validate the results data

        Args:
            results_data (list[dict]):  List of results data to validate

        Raises:
            ValueError: If results_data is not a list
            ValueError: If each sport in results_data is not a dictionary
            ValueError: If each sport does not have exactly the required keys
            ValueError: If any key in a sport does not have the expected type
        """
        logger.debug("Validating results data")
        if not isinstance(results_data, pd.DataFrame):
            raise ValueError("results_data must be a list")
        
        required_headers = {'event_id', 'commence_datetime', 'home_team', 'home_team_score', 'away_team_score', 'away_team'}
        
        if not required_headers.issubset(results_data.columns):
            raise ValueError(f"results_data must have the following headers: {required_headers}")
    
    @transaction.atomic
    def upsert_results(self, results_data: pd.DataFrame) -> int:
        """ Upsert results data into the database

        Args:
            results_data (list[dict]): List of results data to upsert

        Returns:
            int: Number of results upserted
        """
        logger.debug("Upserting results")
        try:
            self.validate_results_data(results_data)
            
            updated_count = 0
            for result_data in results_data:
                result, created = Result.upsert_from_api(result_data)
                if not created:
                    updated_count += 1
            
            logger.debug(f"Upserted {len(results_data)} results, {updated_count} were updates.")
            return len(results_data)
        except Exception as e:
            logger.error(f"Error upserting results: {str(e)}")
            raise
        
    @transaction.atomic
    def get_results(self, **kwargs) -> list[dict]:
        """ Get results data from the database

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            list[dict]: List of results data
        """
        logger.debug(f"Getting sports with filters: {kwargs}")
        results = Result.objects.filter(**kwargs).values() if kwargs else Result.objects.all().values()
        logger.debug(f"Got {len(results)} sports")
        return list(results)
    
    def match_results_to_events(self, results_df: pd.DataFrame, sport: str, source_timezone: str = 'Australia/Sydney') -> pd.DataFrame:
        """
        Match results from a DataFrame to Event IDs in the database.

        Args:
            results_df (pd.DataFrame): DataFrame containing the results data
            source_timezone (str): Timezone of the source data (default: 'Australia/Sydney')

        Returns:
            pd.DataFrame: DataFrame with matched Event IDs
        """
        logger.debug("Matching results to events")
        
        # Convert source timezone to pytz timezone object
        try:
            source_tz = pytz.timezone(source_timezone)
        except pytz.UnknownTimeZoneError as e:
            logger.error(f"Unknown timezone: {source_timezone}")
            raise pytz.UnknownTimeZoneError(f"Unknown timezone: {source_timezone}: {str(e)}")
        
        # Function to find the closest event
        def find_closest_event(row):
            commence_time = source_tz.localize(pd.to_datetime(row['commence_datetime'])).astimezone(pytz.UTC)
            
            # Create a time range for searching (e.g., 24 hours before and after)
            time_range = timedelta(hours=24)
            start_time = commence_time - time_range
            end_time = commence_time + time_range
            
            # Query for potential matching events
            potential_events = Event.objects.filter(
                Q(sport__key=sport) &
                Q(commence_time__range=(start_time, end_time)) &
                (Q(home_team__name__in=[row['home_team'], row['away_team']]) |
                Q(away_team__name__in=[row['home_team'], row['away_team']]))
            )
            
            if not potential_events:
                logger.warning(f"No matching events found for {row['home_team']} vs {row['away_team']} on {commence_time}")
                return None
            else:
                logger.debug(f"Found {len(potential_events)} potential events for {row['home_team']} vs {row['away_team']} on {commence_time}")
            
            # Find the best match considering both time and team names
            best_match = min(
                potential_events,
                key=lambda event: (
                    abs(event.commence_time - commence_time),
                    0 if (event.home_team.name == row['home_team'] and event.away_team.name == row['away_team']) else 1
                )
            )
            
            return best_match.id
        
        # Apply the function to each row
        results_df['event_id'] = results_df.apply(find_closest_event, axis=1)
        
        # Log the matching results
        matched_count = results_df['event_id'].notnull().sum()
        logger.debug(f"Matched {matched_count} out of {len(results_df)} results to events")
        
        return results_df
        
    def __del__(self):
        logger.debug("ResultService terminated")