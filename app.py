from flask import Flask, jsonify, request
from flask_cors import CORS # my plan for getting this on front end
from ForecastClient import ForecastDataClient
from HistoricalClient import HistoricalDataClient
from dotenv import load_dotenv
import os
import json

import numpy as np

import rank

# Initialize app
load_dotenv()
app = Flask(__name__)
# get cors working
CORS(app)

# Initialize clients
forecast_client = ForecastDataClient()
historical_client = HistoricalDataClient(api_key=os.getenv("NOAA_API_KEY"))

@app.route("/")
def home():
    """Root endpoint that confirms the API is running"""
    return jsonify({
        "status": "active",
        "endpoints": {
            "forecast": "/api/forecast?location=<zip_or_city> ",
            "historical": "/api/historical?location=<id>&date=<yyyy-mm-dd>",
            "rank": "/rank?zip_code=26505&search_radius=500"
        }
    })

# forecast route
@app.route("/api/forecast", methods=["GET"])
def get_forecast():
    """
    Get forecast by location (ZIP or City,State)
    Example: /api/forecast?location=princeton,nj
    """
    location = request.args.get("location")
    
    if not location:
        return jsonify({
            "error": "Missing location parameter",
            "example": "/api/forecast?location=princeton,nj"
        }), 400
    
    forecast = forecast_client.get_forecast(location)
    
    if not forecast:
        return jsonify({
            "error": "Unsupported location",
            "available_locations": list(forecast_client.locations.keys()),
            "example_locations": ["princeton,nj", "08540", "new york,ny"]
        }), 400
    
    return jsonify(forecast)

@app.route("/rank", methods=["POST"])
# @app.route("/rank", methods=["GET"])
def rank_request():
    """
    high-level endpoint for ranking launch sites
    Example: /rank
    body: {"zip_code": "8753", "search_radius(mi)": "300", "comparator_weights": {"name": 1, "distance": 1}, "launch": {...}}
    """

    data = request.get_json()

    zip_code = int(request.args.get("zip_code"))
    search_radius = request.args.get("search_radius")
    print (f"Zip code: {zip_code}")
    comparator_weights = data.get("comparator_weights")
    launch = data.get("launch")

    response = rank(zip_code, search_radius, comparator_weights, launch)

    return jsonify(response)

        
@app.route("/api/historical", methods=["GET"])
def get_historical():
    """
    Get historical data by location ID and date
    Example: /api/historical?location=CITY:US360019&date=2023-01-01
    """
    location = request.args.get("location")
    date = request.args.get("date")
    
    if not location or not date:
        return jsonify({
            "error": "Missing parameters",
            "required": ["location", "date"],
            "example": "/api/historical?location=CITY:US360019&date=2023-01-01"
        }), 400
    
    data = historical_client.get_weather_data(location, date)
    return jsonify(data) if data else jsonify({"error": "Data unavailable"}), 500

if __name__ == "__main__":
    # # Test haversine with vectorized inputs
    # lat1 = np.array([40.0, 41.0])
    # lon1 = np.array([-74.0, -75.0])
    # lat2 = np.array([42.0, 43.0])
    # lon2 = np.array([-76.0, -77.0])
    # distances = haversine(lat1, lon1, lat2, lon2)
    # print("Distances:", distances)

    # #test the zip_to_coords function
    # zip = 26505
    # coords = zip_to_coords(zip)
    # if coords is None:
    #     print(f"Zip code {zip} not found")
    # else:
    #     print(f"Coordinates for zip code {zip}: {coords}")

    # #test rank
    # rank()

    app.run(host='0.0.0.0', port=5000, debug=True)