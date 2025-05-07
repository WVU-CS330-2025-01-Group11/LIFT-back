"""
SiteData.py

This module defines the `SiteData` class, which encapsulates metadata for a rocket launch site, including its 
geographic and elevation data. It also provides utility methods for string representation and JSON serialization.

Author:
    Greyson Meares
"""
import numpy as np

# Dict example:
# {'Prefecture Name': 'Tripoli Pittsburgh', 'State': 'PA', 'Latitude': 39.93534, 'Longitude': -79.92406, 'Zip Code': 15410.0, 'Elevation': 1106.0}

class SiteData:
    """
    Class to represent a launch site with its properties and forecast data.
    """
    def __init__(self, site_dictionary):
        self.site_dictionary = site_dictionary
        self.name = site_dictionary.get("Prefecture Name")
        self.zip_code = int(site_dictionary.get("Zip Code"))
        self.latitude = site_dictionary.get("Latitude")
        self.longitude = site_dictionary.get("Longitude")
        self.elevation = site_dictionary.get("Elevation")

        self.max_waiver_altitude = 0

    def __str__(self):
        return f"SiteData(zip_code={self.zip_code}, latitude={self.latitude}, longitude={self.longitude}, elevation={self.elevation})"

    def to_json(self):
        """
        Convert the SiteData object to a JSON-compatible dictionary.
        Returns:
            dict: JSON-compatible dictionary representation of the SiteData object.
        """
        return {
            "name": self.name,
            "zip_code": self.zip_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation": self.elevation,
            "max_waiver_altitude": self.max_waiver_altitude
        }