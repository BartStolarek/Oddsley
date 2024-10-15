import requests

class OddsAPIService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_sports(self):
        response = requests.get(f"{self.base_url}/sports/", params={"apiKey": self.api_key})
        response.raise_for_status()
        return response.json()