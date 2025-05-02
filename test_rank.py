import unittest
from unittest.mock import patch
from rank import rank
from Comparators import (
    distance_comparator,
    windspeed_comparator,
    waiver_altitude_comparator,
    cloud_cover_comparator,
    precipitation_comparator,
    temperature_comparator,
)
from SiteData import SiteData
from ForecastData import ForecastData

class TestRankAndComparators(unittest.TestCase):
    def setUp(self):
        # Example site and forecast data
        self.site1 = SiteData({
            "Prefecture Name": "Site1",
            "Zip Code": 12345,
            "Latitude": 40.0,
            "Longitude": -75.0,
            "Elevation": 100
        })
        self.site2 = SiteData({
            "Prefecture Name": "Site2",
            "Zip Code": 54321,
            "Latitude": 41.0,
            "Longitude": -76.0,
            "Elevation": 200
        })
        self.forecast1 = ForecastData(12345)
        self.forecast2 = ForecastData(54321)
        # Add mock forecast periods if needed
        # For windspeed, temperature, etc., add mock periods
        period1 = type('Period', (), {})()
        period1.temperature = 20
        period1.wind_low = 5
        period1.wind_high = 10
        period1.short_forecast = "Clear"
        period1.percip_prob = 10

        period2 = type('Period', (), {})()
        period2.temperature = 25
        period2.wind_low = 8
        period2.wind_high = 15
        period2.short_forecast = "Cloudy"
        period2.percip_prob = 30

        self.forecast1.forecast_periods = [period1]
        self.forecast2.forecast_periods = [period2]

    def test_distance_comparator(self):
        launch = {'zip': 12345}
        result = distance_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    def test_windspeed_comparator(self):
        launch = {'zip': 12345}
        result = windspeed_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    def test_waiver_altitude_comparator(self):
        launch = {'zip': 12345}
        result = waiver_altitude_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    def test_cloud_cover_comparator(self):
        launch = {'zip': 12345}
        result = cloud_cover_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    def test_precipitation_comparator(self):
        launch = {'zip': 12345}
        result = precipitation_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    def test_temperature_comparator(self):
        launch = {'zip': 12345}
        result = temperature_comparator(launch, self.site1, self.site2, self.forecast1, self.forecast2)
        self.assertIsInstance(result, (int, float))

    @patch("rank.zip_to_coords")
    @patch("rank.sites_in_radius")
    @patch("rank.get_forecast_data")
    def test_rank_overall(self, mock_get_forecast_data, mock_sites_in_radius, mock_zip_to_coords):
        # Mock dependencies for rank
        mock_zip_to_coords.return_value = [40.0, -75.0]
        mock_sites_in_radius.return_value = [
            {
                "Prefecture Name": "Site1",
                "Zip Code": 12345,
                "Latitude": 40.0,
                "Longitude": -75.0,
                "Elevation": 100
            },
            {
                "Prefecture Name": "Site2",
                "Zip Code": 54321,
                "Latitude": 41.0,
                "Longitude": -76.0,
                "Elevation": 200
            }
        ]
        mock_get_forecast_data.side_effect = [self.forecast1, self.forecast2]

        zip_code = 12345
        search_radius = 100
        comparator_weights = {
            "Dist": 1,
            "Temp": 1,
            "Wind S/": 1,
            "Cloud Cover": 1,
            "Precipitation": 1,
            "Waiver Altitude": 1
        }
        launch = {'zip': 12345}
        result = rank(zip_code, search_radius, comparator_weights, launch)
        # result may be a tuple (data, code) or just data depending on your implementation
        self.assertTrue(result is not None)

if __name__ == '__main__':
    unittest.main()