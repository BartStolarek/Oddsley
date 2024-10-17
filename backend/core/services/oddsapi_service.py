import requests
from loguru import logger


class OddsAPIService:
    """ Service class to interact with the OddsAPI
    """
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        logger.debug(f"OddsAPIService initialized with base_url={base_url}")

    def get_sports(self, kwargs) -> list[dict]:
        """ Get sports data from the OddsAPI
        
        Data returned from OddsAPI is a list of dictionaries, each containing information about a sport. 
        
        Response format:
        [
            {
                "key": "americanfootball_ncaaf",
                "group": "American Football",
                "title": "NCAAF",
                "description": "US College Football",
                "active": true,
                "has_outrights": false
            },
            {
                "key": "americanfootball_nfl",
                "group": "American Football",
                "title": "NFL",
                "description": "US Football",
                "active": true,
                "has_outrights": false
            },
            ...
        ]

        Args:
            kwargs (dict): Keyword arguments to pass to the API

        Returns:
            list[dict]: List of sports data
        """
        logger.debug("Getting sports data")
        
        params = {"apiKey": self.api_key}
        
        if kwargs.get('all'):
            logger.debug("Fetching all sports")
            params['all'] = 'true'  # The API expects 'true' as a string, not a boolean
        
        
        # log debug with params but exclude the api key
        logger.debug(f"Requesting sports data with base_url={self.base_url} and params {exclude_api_key(params)}")
        response = requests.get(f"{self.base_url}/sports/", params=params)
        logger.debug(f"Received response with status code {response.status_code}")
        
        # Raise an exception if the request was unsuccessful
        try:
            response.raise_for_status()
            logger.debug(f"Obtained {len(response.json())} sports in response")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error fetching sports data: {e}")
            raise  # Re-raise the exception to be caught in the calling function
        
        return response.json()
    
    def get_events(self, sport, kwargs) -> list[dict]:
        """ Get events data from the OddsAPI for a specified sport

        Data returned from OddsAPI is a list of dictionaries, each containing information about an event.

        Response format:
        [
            {
                "id": "a512a48a58c4329048174217b2cc7ce0",
                "sport_key": "americanfootball_nfl",
                "sport_title": "NFL",
                "commence_time": "2023-01-01T18:00:00Z",
                "home_team": "Atlanta Falcons",
                "away_team": "Arizona Cardinals"
            },
            ...
        ]

        Args:
            sport (str): The sport key obtained from calling the /sports endpoint
            **kwargs: Additional keyword arguments to pass to the API

        Returns:
            list[dict]: List of events data
        """
        logger.debug(f"Getting events data for sport: {sport}")

        params = {"apiKey": self.api_key}

        # Add optional parameters
        if 'dateFormat' in kwargs:
            params['dateFormat'] = kwargs['dateFormat']
        if 'eventIds' in kwargs:
            params['eventIds'] = ','.join(kwargs['eventIds']) if isinstance(kwargs['eventIds'], list) else kwargs['eventIds']
        if 'commenceTimeFrom' in kwargs:
            params['commenceTimeFrom'] = kwargs['commenceTimeFrom']
        if 'commenceTimeTo' in kwargs:
            params['commenceTimeTo'] = kwargs['commenceTimeTo']

        # log debug with params but exclude the api key
        logger.debug(f"Requesting events data with base_url={self.base_url}, sport={sport}, and params {exclude_api_key(params)}")
        response = requests.get(f"{self.base_url}/sports/{sport}/events", params=params)
        logger.debug(f"Received response with status code {response.status_code}")

        # Raise an exception if the request was unsuccessful
        try:
            response.raise_for_status()
            logger.debug(f"Obtained {len(response.json())} events in response")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error fetching events data: {e}")
            raise  # Re-raise the exception to be caught in the calling function

        return response.json()
    
    def get_odds(self, sport, regions, kwargs) -> list[dict]:
        """ Get odds data from the OddsAPI for a specified sport

        Data returned from OddsAPI is a list of dictionaries, each containing information about an event and its odds.

        Args:
            sport (str): The sport key obtained from calling the /sports endpoint
            kwargs (dict): Additional keyword arguments to pass to the API

        Returns:
            list[dict]: List of odds data
        """
        logger.debug(f"Getting odds data for sport: {sport}")

        params = {"apiKey": self.api_key}

        # Add required parameters
        params['sport'] = sport
        params['regions'] = regions
        

        # Add optional parameters
        optional_params = ['markets', 'dateFormat', 'oddsFormat', 'eventIds', 'bookmakers', 
                           'commenceTimeFrom', 'commenceTimeTo']
        for param in optional_params:
            if param in kwargs:
                params[param] = kwargs[param]

        # Handle boolean parameters
        bool_params = ['includeLinks', 'includeSids', 'includeBetLimits']
        for param in bool_params:
            if param in kwargs and kwargs[param]:
                params[param] = 'true'

        # log debug with params but exclude the api key
        logger.debug(f"Requesting odds data with base_url={self.base_url}, sport={sport}, and params {exclude_api_key(params)}")
        response = requests.get(f"{self.base_url}/sports/{sport}/odds/", params=params)
        logger.debug(f"Received response with status code {response.status_code}")

        # Raise an exception if the request was unsuccessful
        try:
            response.raise_for_status()
            logger.debug(f"Obtained odds data for {len(response.json())} events in response")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error fetching odds data: {e}")
            raise  # Re-raise the exception to be caught in the calling function

        return response.json()
    
    def __del__(self):
        logger.debug("OddsAPIService terminated")
        
    
def exclude_api_key(params: dict) -> dict:
    """ Exclude the API key from the parameters dictionary for logging
    
    Args:
        params (dict): The parameters dictionary
    
    Returns:
        dict: The parameters dictionary with the API key excluded
    """
    return {k: v for k, v in params.items() if k != 'apiKey'}