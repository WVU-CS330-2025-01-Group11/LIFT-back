import pytest
from unittest.mock import patch, MagicMock
from ForecastClient import ForecastDataClient
import requests
import numpy as np

# Test data
SAMPLE_FORECAST_DATA = {
    "properties": {
        "forecast": "https://api.weather.gov/forecast/url",
        "elevation": {"value": 50.0}
    }
}

SAMPLE_FORECAST_RESPONSE = {
    "geometry": {
        "coordinates": [[[1,2],[3,4],[5,6],[1,2]]]
    },
    "properties": {
        "elevation": {"value": 50.0},
        "periods": [
            {
                "isDaytime": True,
                "startTime": "2023-01-01T00:00:00",
                "endTime": "2023-01-01T06:00:00",
                "temperature": 50,
                "windSpeed": "10 to 15 mph",
                "shortForecast": "Partly cloudy",
                "probabilityOfPrecipitation": {"value": 20}
            }
        ]
    }
}

class TestForecastDataClient:
    @patch('ForecastClient.APIClient._make_request')
    @patch('ForecastClient.zip_to_coords')
    def test_get_weather_data_success(self, mock_zip_to_coords, mock_make_request):
        """Test successful weather data retrieval with valid coordinates"""
        # Setup
        client = ForecastDataClient()
        mock_make_request.side_effect = [
            SAMPLE_FORECAST_DATA,  # First call for point data
            SAMPLE_FORECAST_RESPONSE  # Second call for forecast data
        ]
        
        # Execute
        result = client.get_weather_data(40.0, -74.0)
        
        # Verify
        assert result == SAMPLE_FORECAST_RESPONSE
        mock_make_request.assert_any_call("https://api.weather.gov/points/40.0,-74.0")
        mock_make_request.assert_any_call("https://api.weather.gov/forecast/url")

    @patch('ForecastClient.APIClient._make_request')
    def test_get_weather_data_failure(self, mock_make_request):
        """Test weather data retrieval failure"""
        # Setup
        client = ForecastDataClient()
        mock_make_request.return_value = None
        
        # Execute
        result = client.get_weather_data(40.0, -74.0)
        
        # Verify
        assert result is None
        mock_make_request.assert_called_once_with("https://api.weather.gov/points/40.0,-74.0")

    @patch('ForecastClient.ForecastDataClient.get_weather_data')
    @patch('ForecastClient.ForecastDataClient.get_coordinates')
    def test_get_forecast_success(self, mock_get_coords, mock_get_weather):
        """Test successful forecast retrieval with valid location"""
        # Setup
        client = ForecastDataClient()
        mock_get_coords.return_value = (40.0, -74.0)
        mock_get_weather.return_value = SAMPLE_FORECAST_RESPONSE
        
        # Execute
        result = client.get_forecast("08540")
        
        # Verify
        assert result == SAMPLE_FORECAST_RESPONSE
        mock_get_coords.assert_called_once_with("08540")
        mock_get_weather.assert_called_once_with(40.0, -74.0)

    @patch('ForecastClient.ForecastDataClient.get_coordinates')
    def test_get_forecast_invalid_location(self, mock_get_coords):
        """Test forecast retrieval with invalid location"""
        # Setup
        client = ForecastDataClient()
        mock_get_coords.return_value = None
        
        # Execute
        result = client.get_forecast("invalid")
        
        # Verify
        assert result is None
        mock_get_coords.assert_called_once_with("invalid")

    @patch('ForecastClient.zip_to_coords')
    def test_get_coordinates_with_zip(self, mock_zip_to_coords):
        """Test coordinate retrieval with ZIP code"""
        # Setup
        client = ForecastDataClient()
        # Add the locations attribute that the method expects
        client.locations = {"08540": (40.0, -74.0)}
        mock_zip_to_coords.return_value = (40.0, -74.0)
        
        # Execute
        result = client.get_coordinates("08540")
        
        # Verify
        assert result == (40.0, -74.0)
        mock_zip_to_coords.assert_called_once_with("08540")

    @patch('ForecastClient.APIClient._make_request')
    def test_request_exception_handling(self, mock_make_request):
        """Test that exceptions are properly handled"""
        # Setup
        client = ForecastDataClient()
        mock_make_request.side_effect = requests.exceptions.RequestException("API Error")
        
        # Execute
        result = client.get_weather_data(40.0, -74.0)
        
        # Verify
        assert result is None