# importing abstract methods
# Some comments ai generated but have been reviewed and are accurate
from abc import ABC, abstractmethod
import requests

"""Abstract base class for api clients, handles http requrests"""
class APIClient(ABC):
    def __init__(self):
        self.session = requests.Session()
    
    @abstractmethod
    def get_weather_data(self, *args, **kwargs):
        """Must be implemented by child classes"""
        pass

    def _make_request(self, url, params=None, headers=None):
        """
        Internal method for making HTTP GET requests.
        
        Args:
            url (str): Endpoint URL
            params (dict): Query parameters
            headers (dict): HTTP headers
            
        Returns:
            dict: JSON response or None if request fails
        """
        try:
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None