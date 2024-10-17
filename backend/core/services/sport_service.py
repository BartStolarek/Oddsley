from django.db import transaction
from core.models import Sport
from loguru import logger


class SportService:
    """ Service class to interact with the Sport model
    """
    
    def __init__(self):
        logger.debug("SportService initialized")
    
    @staticmethod
    def validate_sports_data(sports_data: list[dict]) -> None:
        """_summary_

        Args:
            sports_data (list[dict]): _description_

        Raises:
            ValueError: If sports_data is not a list
            ValueError: If each sport in sports_data is not a dictionary
            ValueError: If each sport does not have exactly the required keys
            ValueError: If any key in a sport does not have the expected type
        """
        logger.debug("Validating sports data")
        if not isinstance(sports_data, list):
            raise ValueError("sports_data must be a list")
        
        required_keys = {"key", "group", "title", "description", "active", "has_outrights"}
        
        for sport in sports_data:
            if not isinstance(sport, dict):
                raise ValueError("Each sport in sports_data must be a dictionary")
            
            if not set(sport.keys()) == required_keys:
                raise ValueError(f"Each sport must have exactly these keys: {required_keys}")
            
            expected_types = {
                'key': str,
                'group': str,
                'title': str,
                'description': str,
                'active': bool,
                'has_outrights': bool
            }
            
            for key, expected_type in expected_types.items():
                if not isinstance(sport.get(key), expected_type):
                    raise ValueError(f"'{key}' must be a {expected_type.__name__}")
        logger.debug("Sports data is valid")

    @transaction.atomic
    def upsert_sports(self, sports_data: list[dict]) -> int:
        """ Upsert sports data into the database

        Args:
            sports_data (list[dict]): List of sports data to upsert

        Returns:
            int: Number of sports upserted
        """
        logger.debug("Upserting sports")
        try:
            self.validate_sports_data(sports_data)
            
            updated_count = 0
            for sport_data in sports_data:
                sport, created = Sport.objects.update_or_create(
                    key=sport_data['key'],
                    defaults={
                        'group': sport_data['group'],
                        'title': sport_data['title'],
                        'description': sport_data['description'],
                        'active': sport_data['active'],
                        'has_outrights': sport_data['has_outrights']
                    }
                )
                if not created:
                    updated_count += 1
            
            logger.debug(f"Upserted {len(sports_data)} sports, {updated_count} were updates.")
            return len(sports_data)
        except Exception as e:
            logger.error(f"Error upserting sports: {str(e)}")
            raise
    
    @transaction.atomic
    def get_sports(self, **kwargs) -> list[dict]:
        """ Get sports data from the database

        Args:
            **kwargs: Arbitrary keyword arguments for filtering

        Returns:
            list[dict]: List of sports data
        """
        logger.debug(f"Getting sports with filters: {kwargs}")
        sports = Sport.objects.filter(**kwargs).values() if kwargs else Sport.objects.all().values()
        logger.debug(f"Got {len(sports)} sports")
        return list(sports)
    
    
    def __del__(self):
        logger.debug("SportService terminated")