from typing import Dict, List
from enum import Enum

def compare_distance(launch: dict, site: dict, forecast: dict) -> float:
    """
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """
    #placeholder
    distance = -42# calculate_distances( launch, site )
    
    return distance

def compare_windspeed(launch: dict, site: dict, forecast: dict) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """
    #placeholder
    windspeed = -42# forecast[ windspeed ]
    
    return windspeed

def compare_waiver_altitude(launch: dict, site: dict, forecast: dict) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (higher = better).
    """
    #placeholder
    max_waiver_altitude = -42# site[ max_waiver_altitude ]
    
    return max_waiver_altitude

def compare_cloud_cover(launch: dict, site: dict, forecast: dict) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """
    #placeholder
    cloud_cover_index = -42# forecast[ cloud_cover_metric ]
    
    return cloud_cover_index

def compare_precipitation(launch: dict, site: dict, forecast: dict) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """

    #placeholder
    forecast_precipitation = -42# forecast[ precipitation ]
    
    return forecast_precipitation

def launch_site_comparator(
    launch: dict, 
    sites_with_forecasts: Dict[str, Dict[str, dict]],
    which: str
) -> List[float]:
    """
    Compares launch sites based on suitability for a given launch.
    
    Args:
        launch: JSON object describing the launch (e.g., payload, target orbit).
        sites_with_forecasts: Dict mapping site IDs to {"site": {...}, "forecast": {...}}.
        which_metric: int 
    
    Returns:
        List[float]: Suitability scores for each site (in input order).
        -1: ERROR: invalid comparison request
    """

    function_map = {

        "DISTANCE": compare_distance,
        "WINDSPEED": compare_windspeed,
        "WAIVER_ALTITUDE": compare_waiver_altitude,
        "CLOUD_COVER": compare_cloud_cover,
        "PRECIPITATION": compare_precipitation
    }

    if which not in function_map:
        raise ValueError( f"Invalid comparison '{which}'." )
        return -1

    suitability_scores = []
    
    for site_id, data in sites_with_forecasts.items():
        site = data["site"]
        forecast = data["forecast"]
        
        score = function_map[ which ](launch, site, forecast)
        suitability_scores.append(score)
    
    return suitability_scores