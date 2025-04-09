import json
import math

example_sites = [
    {"Prefecture Name": "Tripoli Alaska", "Latitude": 61.3707, "Longitude": -152.4044},
    {"Prefecture Name": "Tokyo", "Latitude": 35.682839, "Longitude": 139.759455},
    {"Prefecture Name": "Osaka", "Latitude": 34.693738, "Longitude": 135.502165},
    {"Prefecture Name": "Hokkaido", "Latitude": 43.06417, "Longitude": 141.34694},
]

example_launches = [
    {"Launch Name": "Falcon 9 Block 5", "Latitude": 28.5721, "Longitude": -80.6480},
    {"Launch Name": "Atlas V", "Latitude": 28.5633, "Longitude": -80.5774},
    {"Launch Name": "Electron", "Latitude": -39.2833, "Longitude": 176.5667},
    {"Launch Name": "Soyuz", "Latitude": 46.0, "Longitude": 142.0},
]



example_forecast = [

]

class NameComparator:
    """Comparator for sorting by name."""
    def __call__(self, site1, site2):
        return (site1["Prefecture Name"] > site2["Prefecture Name"]) - (site1["Prefecture Name"] < site2["Prefecture Name"])

def sort (sites, launches, comparator):


class calculate:
    def load_json(filename):
        """Load JSON data from a file."""
        with open(filename, 'r') as file:
            return json.load(file)

    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two GPS points in kilometers."""
        if None in [lat1, lon1, lat2, lon2]:
            return None  # Handle missing data safely

        R = 6371.0  # Earth's radius in km
        phi1, phi2 = map(math.radians, [lat1, lat2])
        delta_phi, delta_lambda = map(math.radians, [lat2 - lat1, lon2 - lon1])

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

class rank:
    def extract_coordinates(data):
        """Extract valid prefectures and their coordinates from JSON data."""
        prefectures, coordinates = [], []

        for item in data:
            name, lat, lon = item.get('Prefecture Name'), item.get('Latitude'), item.get('Longitude')

            if lat is None or lon is None:
                print(f"Skipping {name}: missing coordinates.")
                continue

            prefectures.append(name)
            coordinates.append((lat, lon))

        return prefectures, coordinates


    def calculate_distances(main_location, prefectures, coordinates):
        """Compute distances from the main location to all other prefectures."""
        if main_location not in prefectures:
            raise ValueError(f"Error: '{main_location}' not found in dataset.")

        index = prefectures.index(main_location)
        main_lat, main_long = coordinates[index]

        distances = [
            (prefectures[i], haversine(main_lat, main_long, lat, lon))
            for i, (lat, lon) in enumerate(coordinates) if i != index
        ]

        return sorted(distances, key=lambda x: x[1])  # Sort by distance


    def print_distances(main_location, distances):
        """Print sorted distances from the main location."""
        print(f"\nDistances from {main_location} (sorted by proximity):")
        for loc, dist in distances:
            print(f"{loc}: {dist:.2f} km")


    # --- Main Execution ---
    if __name__ == "__main__":
        main_location = "Tripoli Alaska"
        data = load_json('output.json')

        prefectures, coordinates = extract_coordinates(data)
        sorted_distances = calculate_distances(main_location, prefectures, coordinates)

        print_distances(main_location, sorted_distances)

class comparators: