"""
Rank.py

This module implements the backend logic for ranking rocket launch sites based on a variety of weather and 
location-related criteria. It integrates weather forecasts, geospatial filtering, and multi-criteria decision 
making using user-defined weights.

Author:
    Greyson Meares

NOTICE: file name should be Rank.py
"""
import json
from flask import jsonify
import numpy as np
import pandas as pd

import Comparators
from Comparators import zip_to_coords, sites_in_radius, comp_map, valid_comparators, compare_sites

from ForecastClient import ForecastDataClient
from ForecastData import ForecastData
from SiteData import SiteData

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

    zipcode = site.zip_code
    latitude = site.latitude
    longitude = site.longitude

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
    
    #convert to float
    try:
        search_radius = float(search_radius)
    except ValueError:
        return "invalid search radius", 0, 400

    user_coords = zip_to_coords(zip_code)
    if user_coords is None:
        return "invalid zip code", 0, 400

    if user_coords is None:
        return "invalid zip code", 0, 400

    #get sites in the search radius
    valid_sites = sites_in_radius(user_coords, search_radius)

    site_objects = [SiteData(site) for site in valid_sites]

    # Get forecast data for each valid site
    forcast_data = {}
    for site in site_objects:
        forcast = get_forecast_data(site)

        forcast_data[site] = forcast
        if forcast is None:
            return "invalid forecast data", 0, 400
        
    weight_vector = np.array([comparator_weights[comp] for comp in valid_comparators])

    #normalize the weights      (l^1 norm here because we want to sum to 1)
    weight_vector = weight_vector / np.linalg.norm(weight_vector, ord=1)

    rankings = {}   # Comparator -> List of SiteData

    print ("Running comparators...")
    for key, weight in comparator_weights.items():
        if key not in valid_comparators:
            raise ValueError(f"Invalid comparator: {key}. Valid options are: {valid_comparators}")

        # Call the appropriate ranking function based on the key
        res = compare_sites(launch, forcast_data, key)
        rankings[key] = res

    #compute the average rank for each site using comparator weights
    avg_rankings = {}
    for key, weight in comparator_weights.items():
        for site in rankings[key]:
            if site not in avg_rankings:
                avg_rankings[site] = 0
            avg_rankings[site] += weight * rankings[key].index(site)

    #return list sorted by average rank
    sorted_sites = sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])
    
    return sorted_sites, 200
