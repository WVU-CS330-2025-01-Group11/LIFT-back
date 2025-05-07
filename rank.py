
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
    # zipcode = site["Zip Code"]
    # latitude = site["Latitude"]
    # longitude = site["Longitude"]

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
    # search_radius = data.get("search_radius(mi)")
    #convert to float
    try:
        search_radius = float(search_radius)
    except ValueError:
        return "invalid search radius", 0, 400
    
    # print (f"Search radius: {search_radius}")

    user_coords = zip_to_coords(zip_code)
    if user_coords is None:
        return "invalid zip code", 0, 400

        user_coords = zip_to_coords(zip_code)
    if user_coords is None:
        return "invalid zip code", 0, 400

    #get sites in the search radius
    valid_sites = sites_in_radius(user_coords, search_radius)
    # print (f"Valid sites: {valid_sites}")

    # print (f"User coords: {user_coords}")
    # print (f"Comparator weights: {comparator_weights}")
    # print (f"Launch: {launch}")

    site_objects = [SiteData(site) for site in valid_sites]
    for site in site_objects:
        print (f"Site object: {site}")

    # Get forecast data for each valid site
    forcast_data = {}
    for site in site_objects:
        forcast = get_forecast_data(site)

        forcast_data[site] = forcast
        if forcast is None:
            return "invalid forecast data", 0, 400
        
    # for site, forecast in forcast_data.items():
    #     print (f"Forecast data for SITE: {site.zip_code}: {forecast}")

    weight_vector = np.array([comparator_weights[comp] for comp in valid_comparators])
    print (f"Weight vector: {weight_vector}")

    #normalize the weights      (L^1 norm here because we want to sum to 1)
    weight_vector = weight_vector / np.linalg.norm(weight_vector, ord=1)

    print (f"Normalized weight vector: {weight_vector}")

    # for comp in valid_comparators:
    #     ranking = Comparators.compare_sites(launch, forcast_data, comp) 
    #     print (f"Ranking for {comp}: {ranking}")

    # for each comparator, rank the launch sites
    # using the given weights, find the average rank for each site
    rankings = {}   # Comparator -> List of SiteData

    # optimal_period = {}  # Comparator -> average optimal datetime
    # optimal_period = np.zeros((len(valid_comparators), len(site_objects)))
    optimal_period = []
    print ("Running comparators...")
    for key, weight in comparator_weights.items():
        print (f"Running comparator: {key}, weight: {weight}")
        if key not in valid_comparators:
            raise ValueError(f"Invalid comparator: {key}. Valid options are: {valid_comparators}")
            # return jsonify({"error": f"Invalid comparator: {key}. Valid options are: {valid_comparators}"}), 400

        # Call the appropriate ranking function based on the key
        # compare_sites(launch, forcast_data, key)
        res = compare_sites(launch, forcast_data, key)
        rankings[key] = res[0]
        # optimal_period[valid_comparators.index(key)] = res[1]
        print (f"Optimal period for {key}: {res[1]}")
        optimal_period.append(res[1])

        print (f"Rankings for {key}: ")
        for site in rankings[key]:
            print (f"Site: {site.zip_code}")
        # print (f"Rankings for {key}: {rankings[key]}")
    
    # if any array contained in optimal_period is full of zeros, remove it
    for period in optimal_period:
        if np.all(np.array(period) == 0):
            optimal_period.remove(period)

    #pad the optimal_period list with zeros to make it the same length as the longest list
    max_length = max(len(period) for period in optimal_period)
    for i in range(len(optimal_period)):
        if len(optimal_period[i]) < max_length:
            optimal_period[i] = np.pad(optimal_period[i], (0, max_length - len(optimal_period[i])), 'constant', constant_values=0)

    print (f"Optimal periods: {optimal_period}")

    optimal_period_T = np.array(optimal_period).T

    #compute the average rank for each site using comparator weights
    avg_rankings = {}
    print ("\n\n\n")
    print ("AVERAGing ranks...")
    for key, weight in comparator_weights.items():
        for site in rankings[key]:
            if site not in avg_rankings:
                avg_rankings[site] = 0
            avg_rankings[site] += weight * rankings[key].index(site)

    #print average rankings
    print ("-------------")
    print (f"Average rankings: ")
    for site in avg_rankings:
        print (f"Site: {site.zip_code}, Average rank: {avg_rankings[site]}")

    #return list sorted by average rank
    sorted_sites = sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])
    # print (f"Sorted sites: {sorted_sites}")
    for site in sorted_sites:
        print (f"Site: {site.zip_code}, Average rank: {avg_rankings[site]}")

    print ("\n\n-------------")
    print (f"Optimal times: { optimal_period}")

    # optimal_period: 

    optimal_times = []

    #average each list in optimal_period_T and return the average time for each site
    print (f"Optimal periods transposed: {optimal_period_T}")

    for periods in optimal_period_T:
        print (f"Periods: {periods}")
        optimal_times.append(time_avg(periods))
    
    print ("\n\n-------------")
    print (f"!!!Optimal time!s!!!: {optimal_times}!!!")

    return sorted_sites, optimal_times, 200

def time_avg(time_list):
    """
    Get the average time from a list of times.
    Args:
        time_list (list): List of times to average. 
        ex: [2025-05-08T06:00:00-04:00]
        form: YYYY-MM-DDTHH:MM:SS-04:00
    Returns:
        str: Average time in the format YYYY-MM-DDTHH:MM:SS
    """

    if np.any(np.array(time_list) == 0):
        return 0
    if np.any(np.array(time_list) == None):
        return None
    if len(time_list) < 2:
        return time_list[0]
    

    print (f"Time list: {time_list}")

    time_pd = pd.to_datetime(time_list, utc=True)
    time_pd = time_pd.astype(np.int64)  

    average_time_np = np.average(time_pd)
    average_time_pd = pd.to_datetime(average_time_np)

    print (f"Average time: {average_time_pd}")

    return str(average_time_pd)