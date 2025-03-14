import requests

class APIClient:
    def __init__(self, api_key):
        """
        Initialize the NOAA API client with an API key.

        Args:
            api_key (str): The NOAA API key for authentication.
        """
        self.api_key = api_key
        self.base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

    def fetch_wind_data(self, location_id, start_date, end_date):
        """
        Fetch wind data from the NOAA API for a specific location and date range.

        Args:
            location_id (str): The location ID (e.g., ZIP code or station ID).
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.

        Returns:
            list: A list of wind data points.
        """
        # List of data types to fetch
        data_types = ["AWND", "WDF2", "TAVG"]  # Wind speed, wind direction, and temperature
        results = []

        # Fetch data for each data type individually
        for datatype in data_types:
            params = {
                "datasetid": "GHCND",  # Dataset ID for daily summaries
                "locationid": location_id,  # Location ID (e.g., ZIP code)
                "startdate": start_date,  # Start date for the data range
                "enddate": end_date,  # End date for the data range
                "datatypeid": datatype,  # Data type ID (e.g., AWND for wind speed)
                "limit": 1000,  # Maximum number of data points to return
            }
            headers = {"token": self.api_key}  # Include the API key in the headers

            try:
                print(f"Fetching data for datatype: {datatype}")
                # Make a GET request to the NOAA API
                response = requests.get(self.base_url, headers=headers, params=params)
                response.raise_for_status()  # Raise an error for bad status codes

                # Add the results to the list
                results.extend(response.json()["results"])
                print(f"Successfully fetched data for datatype: {datatype}")
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors (e.g., 400 Client Error)
                print(f"Failed to fetch data for datatype {datatype}: {e}")
            except Exception as e:
                # Handle other errors (e.g., network issues)
                print(f"Error fetching data for datatype {datatype}: {e}")

        return results
