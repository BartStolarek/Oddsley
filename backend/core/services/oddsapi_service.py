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
    
    # Method for when OddsAPIService is finished
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