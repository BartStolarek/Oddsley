from django.db import transaction
from core.models import OddsSnapshot
from loguru import logger


class OddSnapshotService:
    """ Service class to interact with the Event model
    """
    
    def __init__(self):
        logger.debug("OddSnapshotService initialized")
    
    @staticmethod
    def validate_oddssnapshot_data(oddssnapshot_data: list[dict]) -> None:
        """ Validate the oddssnapshotdata

        Args:
            oddssnapshot_data (list[dict]):  List of oddssnapshot data to validate

        Raises:
            ValueError: If oddssnapshot_data is not a list
            ValueError: If each sport in oddssnapshot_data is not a dictionary
            ValueError: If each sport does not have exactly the required keys
            ValueError: If any key in a sport does not have the expected type
        """
        logger.debug("Validating oddssnapshot data")
        if not isinstance(oddssnapshot_data, list):
            raise ValueError("oddssnapshot_data must be a list")
        
        required_keys = {"id", "sport_key", "commence_time", "home_team", "away_team", "bookmakers"}
        
        for snapshot in oddssnapshot_data:
            if not isinstance(snapshot, dict):
                raise ValueError("Each oddssnapshot in oddssnapshot_data must be a dictionary")
            
            if not set(snapshot.keys()) == required_keys:
                raise ValueError(f"Each oddssnapshot must have exactly these keys: {required_keys}")
            
            expected_types = {
                'id': str,
                'sport_key': str,
                'commence_time': str,
                'home_team': str,
                'away_team': str,
                'bookmakers': list
            }
            
            for key, expected_type in expected_types.items():
                if not isinstance(snapshot.get(key), expected_type):
                    raise ValueError(f"'{key}' must be a {expected_type.__name__}")
        logger.debug("oddssnapshot data is valid")

    @transaction.atomic
    def upsert_oddssnapshot(self, oddssnapshot_data: list[dict]) -> int:
        """ Upsert oddssnapshot data into the database

        Args:
            oddssnapshot_data (list[dict]): List of oddssnapshot data to upsert

        Returns:
            int: Number of oddssnapshot upserted
        """
        logger.debug("Upserting oddssnapshot")
        try:
            self.validate_oddssnapshot_data(oddssnapshot_data)
            
            updated_count = 0
            for data in oddssnapshot_data:
                obj, created = OddsSnapshot.update_or_create_from_api(data)
                if not created:
                    updated_count += 1
            
            logger.debug(f"Upserted {len(oddssnapshot_data)} oddssnapshot, {updated_count} were updates.")
            return len(oddssnapshot_data)
        except Exception as e:
            logger.error(f"Error upserting oddssnapshot: {str(e)}")
            raise
        
    @transaction.atomic
    def get_oddssnapshot(self, **kwargs) -> list[dict]:
        """ Get oddssnapshot data from the database

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            list[dict]: List of oddssnapshot data
        """
        logger.debug(f"Getting sports with filters: {kwargs}")
        oddssnapshot = OddsSnapshot.objects.filter(**kwargs).values() if kwargs else OddsSnapshot.objects.all().values()
        logger.debug(f"Got {len(oddssnapshot)} sports")
        return list(oddssnapshot)
        
    def __del__(self):
        logger.debug("OddsSnapshotService terminated")