from typing import Dict, List
from enum import Enum
from ForecastData import ForecastData
from rank import haversine, zip_to_coords

def distance_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
    """
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """
    #placeholder

    launchCoords = zip_to_coords( launch[ zip ] )
    siteCoords = zip_to_coords( site[ zip ] )
    distance = haversine( launchCoords[ 0 ], launchCoords[ 1 ], siteCoords[ 0 ], siteCoords[ 1 ] )
    
    return distance

def windspeed_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float[]: each period's windspeed (lower = better).
    """
    result = []

    for period in ForecastData.forecast_periods:
        result.append( period.wind_speed )
    
    return result

def waiver_altitude_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
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

def cloud_cover_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
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

def precipitation_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
    """
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float[]: Each period's expected precipitation (lower = better).
    """

    result = []

    for period in ForecastData.forecast_periods:
        result.append( period.percip )
    
    return result

def temperature_comparator( launch: dict, site: dict, forecast: ForecastData ) -> float:
    """    
    Args:
        launch: JSON object containing launch details.
        site: JSON object containing launch site details.
        forecast: JSON object containing forecast data for the site.
    
    Returns:
        float: Suitability score (lower = better).
    """

    result = []

    for period in ForecastData.forecast_periods:
        result.append( period.temperature )
    
    return result

def compare_sites(
    launch: dict, 
    sites_with_forecasts: Dict[ str, Dict[ str, dict ] ],
    which: str
) -> List[ float ]:
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

        "DISTANCE": distance_comparator,
        "WINDSPEED": windspeed_comparator,
        "WAIVER_ALTITUDE": waiver_altitude_comparator,
        "CLOUD_COVER": cloud_cover_comparator,
        "PRECIPITATION": precipitation_comparator,
        "TEMPERATURE": temperature_comparator
    }

    if which not in function_map:
        raise ValueError( f"Invalid comparison '{which}'." )
        return -1

    suitability_scores = []
    
    for site_id, data in sites_with_forecasts.items():
        site = data[ "site" ]
        forecast = data[ "forecast" ]
        
        score = function_map[ which ]( launch, site, forecast )
        suitability_scores.append( score )
    
    return suitability_scores