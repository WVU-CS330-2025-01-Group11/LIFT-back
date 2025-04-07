from APIClient import APIClient

class ForecastDataClient(APIClient):
    """Client for retrieving weather forecast data"""
    def __init__(self):
        """Initialize with predefined locations and endpoints"""
        super().__init__()
        self.base_url = "https://api.weather.gov"
        # just some random locations for now while we get things rolling
        self.locations = {
            "08540": (40.3573, -74.6672),
            "90210": (34.1030, -118.4108),
            "10001": (40.7506, -73.9975),
            "princeton,nj": (40.3573, -74.6672),
            "new york,ny": (40.7128, -74.0060),
            "miami,fl": (25.7617, -80.1918)
        }

    def get_weather_data(self, latitude, longitude):
        """
        Retrieve forecast data for specific coordinates
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            
        Returns:
            dict: Forecast data or None if request fails
        """
        try:
            point_url = f"{self.base_url}/points/{latitude},{longitude}"
            point_data = self._make_request(point_url)
            if not point_data:
                return None
            forecast_url = point_data["properties"]["forecast"]
            return self._make_request(forecast_url)
        except Exception as e:
            print(f"Forecast error: {e}")
            return None

    def get_forecast(self, location_input):
        """
        User-friendly forecast retrieval by location name/ZIP.
        
        Args:
            location_input (str): ZIP code or "City,State" format
            
        Returns:
            dict: Forecast data or None if location is invalid
        """
        coords = self.get_coordinates(location_input.lower().strip())
        if not coords:
            return None
        return self.get_weather_data(*coords)

    def get_coordinates(self, location_input):
        """
        Helper method to convert location input to coordinates.
        
        Args:
            location_input (str): Normalized location string
            
        Returns:
            tuple: (latitude, longitude) or None if not found
        """
        return self.locations.get(location_input)