
import json
import numpy as np

import Comparators
from Comparators import zip_to_coords, sites_in_radius

from ForecastClient import ForecastDataClient
from ForecastData import ForecastData
from SiteData import SiteData

valid_comparators = ["Dist", "Temp", "Wind S/", "Cloud Cover", "Precipitation", "WaiverAltitude"]
comparators = [Comparators.distance_comparator, 
               Comparators.temperature_comparator,
               Comparators.windspeed_comparator,
               Comparators.cloud_cover_comparator,
               Comparators.precipitation_comparator,
               Comparators.waiver_altitude_comparator]

comp_map = dict(zip(valid_comparators, comparators))


#initializing the forecast client
forcast_client = ForecastDataClient()

def get_forecast_data(site):
    """
    Get forecast data for a given location
    Args:
        location (str): Location ID (e.g., "CITY:US360019")
    Returns:
        dict: Forecast data for the location
    """
    zipcode = site["Zip Code"]
    latitude = site["Latitude"]
    longitude = site["Longitude"]

    #create forcast data object
    forecast_data = ForecastData(zipcode)
    forecast_dict = forcast_client.get_weather_data(latitude, longitude)

    if not forecast_dict:
        return None
    
    forecast_data.from_dict(forecast_dict)

    print (f"Forecast data for {zipcode}: {forecast_data}")

    return forecast_data

def rank(zip_code, search_radius, comparator_weights, launch):

    # Check if the search radius is valid
    # search_radius = data.get("search_radius(mi)")
    #convert to float
    try:
        search_radius = float(search_radius)
    except ValueError:
        return "invalid search radius", 400
    
    print (f"Search radius: {search_radius}")

    user_coords = zip_to_coords(zip_code)
    if user_coords is None:
        return "invalid zip code", 400

    #get sites in the search radius
    valid_sites = sites_in_radius(user_coords, search_radius)
    print (f"Valid sites: {valid_sites}")

    print (f"User coords: {user_coords}")
    print (f"Comparator weights: {comparator_weights}")
    print (f"Launch: {launch}")

    site_objects = [SiteData(site) for site in valid_sites]
    for site in site_objects:
        print (f"Site object: {site}")

    # Get forecast data for each valid site
    forcast_data = {}
    for site in valid_sites:
        forcast = get_forecast_data(site)

        forcast_data[site["Zip Code"]] = forcast
        if forcast is None:
            return "invalid forecast data", 400
        
    print (f"Forecast data: {forcast_data}")

    weight_vector = np.array([comparator_weights[comp] for comp in valid_comparators])
    print (f"Weight vector: {weight_vector}")

    #normalize the weights      (L^1 norm here because we want to sum to 1)
    weight_vector = weight_vector / np.linalg.norm(weight_vector, ord=1)

    print (f"Normalized weight vector: {weight_vector}")
   

    # for each comparator, rank the launch sites
    # using the given weights, find the average rank for each site    
    # for key, weight in comparator_weights.items():
    #     if key not in valid_comparators:
    #         return jsonify({"error": f"Invalid comparator: {key}. Valid options are: {valid_comparators}"}), 400
        

    #     # Call the appropriate ranking function based on the key
    #     rank_low(sites, launch, comparator_weights[key])

    # # return just the valid sites for now
    
    # valid_sites = valid_sites
      