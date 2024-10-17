from django.db import transaction
from core.models import Event
from loguru import logger


class EventService:
    """ Service class to interact with the Event model
    """
    
    def __init__(self):
        logger.debug("eventservice initialized")
    
    @staticmethod
    def validate_events_data(events_data: list[dict]) -> None:
        """ Validate the events data

        Args:
            events_data (list[dict]):  List of events data to validate

        Raises:
            ValueError: If events_data is not a list
            ValueError: If each sport in events_data is not a dictionary
            ValueError: If each sport does not have exactly the required keys
            ValueError: If any key in a sport does not have the expected type
        """
        logger.debug("Validating events data")
        if not isinstance(events_data, list):
            raise ValueError("events_data must be a list")
        
        required_keys = {"key", "group", "title", "description", "active", "has_outrights"}
        
        for event in events_data:
            if not isinstance(event, dict):
                raise ValueError("Each event in events_data must be a dictionary")
            
            if not set(event.keys()) == required_keys:
                raise ValueError(f"Each event must have exactly these keys: {required_keys}")
            
            expected_types = {
                'id': str,
                'sport_key': str,
                'sport_title': str,
                'commence_time': str,
                'home_team': str,
                'away_team': str
            }
            
            for key, expected_type in expected_types.items():
                if not isinstance(event.get(key), expected_type):
                    raise ValueError(f"'{key}' must be a {expected_type.__name__}")
        logger.debug("events data is valid")

    @transaction.atomic
    def upsert_events(self, events_data: list[dict]) -> int:
        """ Upsert events data into the database

        Args:
            events_data (list[dict]): List of events data to upsert

        Returns:
            int: Number of events upserted
        """
        logger.debug("Upserting events")
        try:
            self.validate_events_data(events_data)
            
            updated_count = 0
            for event_data in events_data:
                event, created = Event.update_or_create_from_api(event_data)
                if not created:
                    updated_count += 1
            
            logger.debug(f"Upserted {len(events_data)} events, {updated_count} were updates.")
            return len(events_data)
        except Exception as e:
            logger.error(f"Error upserting events: {str(e)}")
            raise
        
    def __del__(self):
        logger.debug("EventService terminated")