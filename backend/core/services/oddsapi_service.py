import requests
from loguru import logger
from datetime import datetime


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
            {s
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
    
    def get_events(self, sport, **kwargs) -> list[dict]:
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
    
    def get_historical_events(self, sport, date, **kwargs) -> list[dict]:
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
        logger.debug(f"Getting historical events data for sport: {sport}")

        params = {
            "apiKey": self.api_key,
            "date": date.isoformat() + "Z"
        }

        # Add optional parameters
        for key, value in kwargs.items():
            if key in ["dateFormat", "eventIds", "commenceTimeFrom", "commenceTimeTo"]:
                if isinstance(value, list):
                    params[key] = ",".join(value)
                elif isinstance(value, datetime):
                    params[key] = value.isoformat() + "Z"
                else:
                    params[key] = value

        # log debug with params but exclude the api key
        logger.debug(f"Requesting events data with base_url={self.base_url}, sport={sport}, and params {exclude_api_key(params)}")
        response = requests.get(f"{self.base_url}/historical/sports/{sport}/events", params=params)
        logger.debug(f"Received response with status code {response.status_code}")

        # Raise an exception if the request was unsuccessful
        try:
            response.raise_for_status()
            logger.debug(f"Obtained {len(response.json()['data'])} events in response")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error fetching events data: {e}")
            raise  # Re-raise the exception to be caught in the calling function

        return response.json()
    
    def get_historical_odds(self, sport, regions, markets, date, **kwargs) -> dict:
        """ Get historical odds data from the OddsAPI

        Data returned from OddsAPI is a dictionary containing information about historical odds.

        Response format:
        {
            "timestamp": "2023-11-29T22:40:39Z",
            "previous_timestamp": "2023-11-29T22:35:39Z",
            "next_timestamp": "2023-11-29T22:45:40Z",
            "data": {
                "id": "da359da99aa27e97d38f2df709343998",
                "sport_key": "basketball_nba",
                "sport_title": "NBA",
                "commence_time": "2023-11-30T00:10:00Z",
                "home_team": "Detroit Pistons",
                "away_team": "Los Angeles Lakers",
                "bookmakers": [
                    {
                        "key": "draftkings",
                        "title": "DraftKings",
                        "last_update": "2023-11-29T22:40:09Z",
                        "markets": [
                            {
                                "key": "h2h_q1",
                                "last_update": "2023-11-29T22:40:55Z",
                                "outcomes": [
                                    {
                                        "name": "Detroit Pistons",
                                        "price": 2.5
                                    },
                                    {
                                        "name": "Los Angeles Lakers",
                                        "price": 1.56
                                    }
                                ]
                            },
                            {
                                "key": "player_points",
                                "last_update": "2023-11-29T22:40:55Z",
                                "outcomes": [
                                    {
                                        "name": "Over",
                                        "description": "Anthony Davis",
                                        "price": 1.83,
                                        "point": 23.5
                                    },
                                    {
                                        "name": "Under",
                                        "description": "Anthony Davis",
                                        "price": 1.91,
                                        "point": 23.5
                                    },
                                    {
                                        "name": "Over",
                                        "description": "Ausar Thompson",
                                        "price": 1.87,
                                        "point": 11.5
                                    },
                                    {
                                        "name": "Under",
                                        "description": "Ausar Thompson",
                                        "price": 1.87,
                                        "point": 11.5
                                    },
                                    {
                                        "name": "Over",
                                        "description": "Cade Cunningham",
                                        "price": 1.91,
                                        "point": 23.5
                                    },
                                    {
                                        "name": "Under",
                                        "description": "Cade Cunningham",
                                        "price": 1.83,
                                        "point": 23.5
                                    },
                                    {
                                        "name": "Over",
                                        "description": "D'Angelo Russell",
                                        "price": 1.87,
                                        "point": 14.5
                                    },
                                    ...

        Args:
            **kwargs: Additional keyword arguments to pass to the API

        Returns:
            dict: Historical odds data
        """
        
        
        
        params = {
            "apiKey": self.api_key,
        }
        
        params['regions'] = ",".join(regions) if isinstance(regions, list) else regions
        params['markets'] = ",".join(markets) if isinstance(markets, list) else markets
        params['date'] = date.isoformat() + "Z"
        
        
        # Add optional parameters
        for key, value in kwargs.items():
            if key in ["dateFormat", "oddsFormat", "eventIds", "bookmakers", 
                       "commenceTimeFrom", "commenceTimeTo", "includeLinks", 
                       "includeSids", "IncludeBetLimits"]:
                if isinstance(value, list):
                    params[key] = ",".join(value)
                elif isinstance(value, datetime):
                    params[key] = value.isoformat() + "Z"
                else:
                    params[key] = value

        url = f"{self.base_url}/historical/sports/{sport}/odds"
        
        logger.debug(f"Requesting historical odds data with base_url={self.base_url}, sport={sport}, and params {exclude_api_key(params)}")

        response = requests.get(url=url, params=params)
        logger.debug(f"Received response with status code {response.status_code}, token requests used: {response.headers.get('x-requests-used')}, token requests remaining: {response.headers.get('x-requests-remaining')}, last request used: {response.headers.get('x-requests-last')} tokens")
        
        response.raise_for_status()
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