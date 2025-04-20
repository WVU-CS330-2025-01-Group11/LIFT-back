import json
import numpy as np

#get sites and the coords
with open("List of Launch Sites/output.json", "r") as f:
    sites = json.load(f)

    sites_lat = np.array([site["Latitude"] for site in sites])
    sites_lon = np.array([site["Longitude"] for site in sites])

    #get rid of the None values
    sites_lat = np.array([lat for lat in sites_lat if lat is not None])
    sites_lon = np.array([lon for lon in sites_lon if lon is not None])

    #get ride of sites with no lat/lon
    sites = np.array([site for site in sites if site["Latitude"] is not None and site["Longitude"] is not None])
    #convert to numpy arrays
    sites_lat = np.array(sites_lat, dtype=float)
    sites_lon = np.array(sites_lon, dtype=float)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two GPS points in kilometers."""

    """ Slight modification to the original to handle vectorized inputs """


    if np.nan in [lat1.any(), lon1.any(), lat2.any(), lon2.any()]:
        return np.nan
    if None in [lat1.any(), lon1.any(), lat2.any(), lon2.any()]:
        return None
    # Handle missing data safely
    
    # # Ensure all inputs are numpy arrays for vectorized operations and they are of the same shape
    # lat1, lon1, lat2, lon2 = map(np.asarray, [lat1, lon1, lat2, lon2])
    if lat1.shape != lat2.shape or lon1.shape != lon2.shape:
        raise ValueError("Input arrays must have the same shape.")

    R = 6371.0 * np.ones_like(lat1)  # Earth's radius in km
    # phi1, phi2 = np.map(np.radians, [lat1, lat2])
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    # delta_phi, delta_lambda = map(np.radians, [lat2 - lat1, lon2 - lon1])
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

def zip_to_coords(zip_code):
    """
    Convert a zip code to coordinates using the US_zip_codes.npy, US_coordinates.npy files
    """
    # Load the numpy arrays
    zip_codes = np.load("List of Launch Sites/US_zip_codes.npy")
    coordinates = np.load("List of Launch Sites/US_coordinates.npy")

    # Find the index of the zip code
    index = np.where(zip_codes == zip_code)[0]

    if index.size == 0:
        return None  # Zip code not found

    # Return the coordinates as numpy array of floats
    return coordinates[index[0]].astype(float)


def sites_in_radius(user_coords, search_radius):
    #From the stored sites, return all that are within the search radius of user_coords

    # I think this is minimal explicit use of for loops.
    # Hopefully should be significantly faster than a naive implementation,
    # at the expense of some readability. I can probably answer most questions about it.

    user_lat, user_lon = user_coords[0] * np.ones_like(sites_lat), user_coords[1] * np.ones_like(sites_lon)
    
    #ensure dtype is float
    user_lat, user_lon = user_lat.astype(float), user_lon.astype(float)
    fsites_lat, fsites_lon = sites_lat.astype(float), sites_lon.astype(float)

    #calculate the distance to each site
    distances = haversine(user_lat, user_lon, fsites_lat, fsites_lon)

    #get the sites within the search radius
    return sites[distances <= search_radius]