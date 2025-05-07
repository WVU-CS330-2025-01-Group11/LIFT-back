from typing import Dict, List
from enum import Enum
import numpy as np
import json
from functools import cmp_to_key

import pandas as pd

from ForecastData import ForecastData
from SiteData import SiteData

from Utility import haversine, zip_to_coords, sites_in_radius

def distance_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on distance from the launch location."""
    launch_zip = launch['zip']
    launch_coords = zip_to_coords(launch_zip)

    site_coords1 = np.array([site1.latitude, site1.longitude])
    site_coords2 = np.array([site2.latitude, site2.longitude])
    
    # site_coords1 = zip_to_coords(site1.zip)
    # site_coords2 = zip_to_coords(site2.zip)
    
    distance1 = haversine(launch_coords[0], launch_coords[1], site_coords1[0], site_coords1[1])
    distance2 = haversine(launch_coords[0], launch_coords[1], site_coords2[0], site_coords2[1])
    
    if distance1 < distance2:
        return -1, 0  # site1 is better (closer)
    elif distance1 > distance2:
        return 1, 0   # site2 is better
    else:
        return 0, 0

def windspeed_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on average wind speed (lower is better)."""
    # avg_wind1 = sum(0.5 * (p.wind_low + p.wind_high) for p in forecast1.forecast_periods) / len(forecast1.forecast_periods)
    # avg_wind2 = sum(0.5 * (p.wind_low + p.wind_high) for p in forecast2.forecast_periods) / len(forecast2.forecast_periods)
    low_speeds1 = [float(p.wind_low) for p in forecast1.forecast_periods]
    high_speeds1 = [float(p.wind_high) for p in forecast1.forecast_periods]
    low_speeds2 = [float(p.wind_low) for p in forecast2.forecast_periods]
    high_speeds2 = [float(p.wind_high) for p in forecast2.forecast_periods]

    p = 1  # L^1 norm (sum of absolute values)

    norm_low1 = np.linalg.norm(low_speeds1, ord=p)
    norm_high1 = np.linalg.norm(high_speeds1, ord=p)
    norm_low2 = np.linalg.norm(low_speeds2, ord=p)
    norm_high2 = np.linalg.norm(high_speeds2, ord=p)

    # print (f"Low speeds 1: {low_speeds1}, High speeds 1: {high_speeds1}")
    # print (f"Low speeds 2: {low_speeds2}, High speeds 2: {high_speeds2}")
    # print (f"Norm low 1: {norm_low1}, Norm high 1: {norm_high1}")
    # print (f"Norm low 2: {norm_low2}, Norm high 2: {norm_high2}")

    low_weight = 0.2
    high_weight = 0.8

    low_weight, high_weight = np.array([low_weight, high_weight]) / np.linalg.norm([low_weight, high_weight], ord=1)
    avg_wind1 = low_weight * norm_low1 + high_weight * norm_high1
    avg_wind2 = low_weight * norm_low2 + high_weight * norm_high2
    # print (f"Avg wind 1: {avg_wind1}, Avg wind 2: {avg_wind2}")
    
    if avg_wind1 < avg_wind2:
        optimal_period = forecast1.forecast_periods[low_speeds1.index(min(low_speeds1))].start
        return -1, optimal_period  # site1 is better (lower wind speed)
    elif avg_wind1 > avg_wind2:
        optimal_period = forecast2.forecast_periods[low_speeds2.index(min(low_speeds2))].start
        return 1, optimal_period  # site2 is better
    else:
        return 0, 0

def waiver_altitude_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on maximum waiver altitude (higher is better)."""
    waiver1 = site1.max_waiver_altitude
    waiver2 = site2.max_waiver_altitude
    
    if waiver1 > waiver2:
        return -1, 0   # site1 is better (higher waiver altitude)
    elif waiver1 < waiver2:
        return 1, 0
    else:
        return 0, 0

def cloud_cover_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on cloud cover (lower is better)."""
    # cloud1 = forecast1.cloud_cover_metric
    # cloud2 = forecast2.cloud_cover_metric

    # For cloud cover metric we will need to parse the short forecast string

    return 0, 0  # Placeholder for actual cloud cover comparison logic


    if cloud1 < cloud2:
        return -1   # site1 is better (lower cloud cover)
    elif cloud1 > cloud2:
        return 1
    else:
        return 0

def precipitation_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on precipitation probability (lower is better)."""
    # avg_precip1 = sum(p.percip_prob for p in forecast1.forecast_periods) / len(forecast1.forecast_periods)
    # avg_precip2 = sum(p.percip_prob for p in forecast2.forecast_periods) / len(forecast2.forecast_periods)

    precip_probs1 = [float(p.percip_prob) for p in forecast1.forecast_periods]
    precip_probs2 = [float(p.percip_prob) for p in forecast2.forecast_periods]

    p = 1  # L^1 norm (sum of absolute values)
    avg_precip1 = np.linalg.norm(precip_probs1, ord=p)
    avg_precip2 = np.linalg.norm(precip_probs2, ord=p)
    
    if avg_precip1 < avg_precip2:
        # optimal_period = precip_probs1.index(min(precip_probs1))
        optimal_period = forecast1.forecast_periods[precip_probs1.index(min(precip_probs1))].start
        return -1, optimal_period  # site1 is better (lower precipitation probability)
    elif avg_precip1 > avg_precip2:
        # optimal_period = precip_probs2.index(min(precip_probs2))
        optimal_period = forecast2.forecast_periods[precip_probs2.index(min(precip_probs2))].start
        return 1, optimal_period  # site2 is better
    else:
        return 0, 0

def temperature_comparator(launch: dict, site1: SiteData, site2: SiteData, forecast1: ForecastData, forecast2: ForecastData) -> float:
    """Compare two sites based on temperature (lower is better)."""
    # avg_temp1 = sum(p.temperature for p in forecast1.forecast_periods) / len(forecast1.forecast_periods)
    # avg_temp2 = sum(p.temperature for p in forecast2.forecast_periods) / len(forecast2.forecast_periods)
    
    temps1 = [float(p.temperature) for p in forecast1.forecast_periods]
    temps2 = [float(p.temperature) for p in forecast2.forecast_periods]

    p = 1  # L^1 norm (sum of absolute values)
    avg_temp1 = np.linalg.norm(temps1, ord=p)
    avg_temp2 = np.linalg.norm(temps2, ord=p)

    if avg_temp1 < avg_temp2:
        # optimal_period = temps1.index(min(temps1))
        optimal_period = forecast1.forecast_periods[temps1.index(min(temps1))].start
        return -1, optimal_period  # site1 is better (lower temperature)
    elif avg_temp1 > avg_temp2:
        # optimal_period = temps2.index(min(temps2))
        optimal_period = forecast2.forecast_periods[temps2.index(min(temps2))].start
        return 1, optimal_period
    else:
        return 0, 0

valid_comparators = ["Dist", "Temp", "Wind S/", "Cloud Cover", "Precipitation", "Waiver Altitude"]
comparators = [
    distance_comparator,
    temperature_comparator,
    windspeed_comparator,
    cloud_cover_comparator,
    precipitation_comparator,
    waiver_altitude_comparator
]

comp_map = dict(zip(valid_comparators, comparators))

def compare_sites(
    launch: dict, 
    sites_with_forecasts: Dict[SiteData, ForecastData],
    which: str
) -> List[SiteData]:
    """
    Compares launch sites based on suitability for a given launch and returns them sorted.
    
    Args:
        launch: JSON object describing the launch.
        sites_with_forecasts: Dictionary mapping sites to their forecast data.
        which: Metric to compare by.
    
    Returns:
        List[SiteData]: Sorted list of sites from most to least suitable.
    """
    if which not in comp_map:
        raise ValueError(f"Invalid comparison '{which}'.")
    
    # Convert to list of tuples (SiteData, ForecastData)
    sites_list = list(sites_with_forecasts.items())
    
    comparator_func = comp_map[which]

    optimal_periods = []
    
    # Define comparison function for sorting
    def compare(a, b):
        (site_a, forecast_a) = a
        (site_b, forecast_b) = b
        res = comparator_func(launch, site_a, site_b, forecast_a, forecast_b)
        optimal_periods.append(res[1])
        # optimal_period_indices.append(time_avg([res[1]]))
        return res[0]
    
    # Sort using the comparator
    sorted_sites = sorted(sites_list, key=cmp_to_key(compare))

    # optimal_avg_period = time_avg(optimal_periods)
    # print (f"Optimal average period: {optimal_avg_period}")
    
    # Extract the SiteData objects in order
    return [site for (site, _) in sorted_sites], optimal_periods

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
    
    #remove invalid times
    time_list = [t for t in time_list if t != 0 and t is not None]

    print (f"Time list: {time_list}")

    time_pd = pd.to_datetime(time_list, utc=True)
    time_pd = time_pd.astype(np.int64)  

    average_time_np = np.average(time_pd)
    average_time_pd = pd.to_datetime(average_time_np)

    print (f"Average time: {average_time_pd}")

    return str(average_time_pd)

