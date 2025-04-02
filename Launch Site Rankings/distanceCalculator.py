import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two GPS points (latitude, longitude) in kilometers.

    Uses the haversine formula

    Parameters:
    lat1, lon1 -- Latitude and longitude of the first point in decimal degrees.
    lat2, lon2 -- Latitude and longitude of the second point in decimal degrees.

    Returns:
    Distance between the two points in kilometers.
    """
    # Radius of the Earth in km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in km
    distance = R * c
    return distance, distance / 1.609

# Example usage
# GPS coordinates of two locations (lat, lon)
point1 = (39.644869357985215, -79.97182979934257)
point2 = (39.63541857659106, -79.9571305422692)   

km, miles = haversine(*point1, *point2)
print(f"Distance: {km:.2f} km, {miles:.2f} miles")