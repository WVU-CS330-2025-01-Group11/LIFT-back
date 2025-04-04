from APIClient import APIClient
from datetime import datetime

class HistoricalDataClient(APIClient):
    """
    Client for retrieving historical weather data
    might delete later if we don't implement what it would be used for
    this will make me sad :(
    """
    def __init__(self, api_key):
        super().__init__()
        self.base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
        self.headers = {"token": api_key}
    
    def get_weather_data(self, location_id, date):
        params = {
            "datasetid": "GHCND",
            "locationid": location_id,
            "startdate": date,
            "enddate": date,
            "limit": 1000
        }
        return self._make_request(self.base_url, params=params, headers=self.headers)