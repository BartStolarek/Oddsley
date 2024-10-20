from django.db import transaction
from core.models import Odd
from loguru import logger
from datetime import datetime



class OddService:
    """ Service class to interact with the Odd model
    """
    
    def __init__(self):
        logger.debug("oddservice initialized")
    
    @staticmethod
    def validate_odds_data(data: list[dict]) -> None:
        """ Validate the odds data

        Args:
            odds_data (list[dict]):  List of odds data to validate

        Raises:
            ValueError: If odds_data is not a list
            ValueError: If each sport in odds_data is not a dictionary
            ValueError: If each sport does not have exactly the required keys
            ValueError: If any key in a sport does not have the expected type
        """
        logger.debug("Validating odds data")
        
        if not isinstance(data, list):
            raise ValueError("odds_data['data'] must be a list")
        
        required_odds_keys = {"id", "sport_key", "sport_title", "commence_time", "home_team", "away_team", "bookmakers"}
        
        for odd in data:
            if not isinstance(odd, dict):
                raise ValueError("Each odd in odds_data must be a dictionary")
            
            if not set(odd.keys()) == required_odds_keys:
                raise ValueError(f"Each odd must have exactly these keys: {required_odds_keys}")
            
            expected_types = {
                'id': str,
                'sport_key': str,
                'sport_title': str,
                'commence_time': str,
                'home_team': str,
                'away_team': str,
                'bookmakers': list
            }
            
            for key, expected_type in expected_types.items():
                if not isinstance(odd.get(key), expected_type):
                    raise ValueError(f"'{key}' must be a {expected_type.__name__}")
        logger.debug("odds data is valid")

    @transaction.atomic
    def upsert_odds(self, data: list[dict], **kwargs) -> int:
        """ Upsert odds data into the database

        Args:
            odds_data (list[dict]): List of odds data to upsert

        Returns:
            int: Number of odds upserted
        """
        logger.debug("Upserting odds")
        try:
            self.validate_odds_data(data)
        except ValueError as e:
            logger.error(f"Error validating odds data: {str(e)}")
            raise
        
        updated_count = 0
        created_count = 0
        
        
        for odd in data:
            try:
                obj, created = Odd.upsert_from_api(odd, **kwargs)
            except Exception as e:
                logger.error(f"Error upserting odd: {str(e)}, data: {odd}")
            if not created:
                updated_count += 1
            else:
                created_count += 1
        total_count = updated_count + created_count
        logger.debug(f"Upserted {total_count} odds, {created_count} were created and {updated_count} were updated.")
        return total_count
        
    
    @transaction.atomic
    def get_odds(self, **kwargs) -> list[dict]:
        """ Get odds data from the database

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            list[dict]: List of odds data
        """
        logger.debug(f"Getting sports with filters: {kwargs}")
        odds = Odd.objects.filter(**kwargs).values() if kwargs else Odd.objects.all().values()
        logger.debug(f"Got {len(odds)} sports")
        return list(odds)
        
    def __del__(self):
        logger.debug("OddService terminated")