# TODO file description good coumentation
from flask import Flask, jsonify, request
from flask_cors import CORS # my plan for getting this on front end
from ForecastClient import ForecastDataClient
from dotenv import load_dotenv
import os
import json

import numpy as np

import Rank

# Initialize app
load_dotenv()
app = Flask(__name__)

# get cors working
frontend_url = os.environ.get('FRONTEND_URL', 'https://yellow-river-000fe9d0f.6.azurestaticapps.net')
CORS(app, resources={r"/*": {"origins": "frontend_url"}})

# Initialize clients
forecast_client = ForecastDataClient()

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
def rank_request():
    """
    high-level endpoint for ranking launch sites
    Example: /rank?zip_code=26505&search_radius=500
    body: {"comparator_weights": {"name": 1, "distance": 1}, "launch": {...}}
    """

    data = request.get_json()

    if not data:
        print ("No data provided")
        return jsonify({"error": "No data provided"}), 400

    zip_code = int(request.args.get("zip_code"))
    search_radius = request.args.get("search_radius")

    comparator_weights = data[0]
    launch = data[1]

    ranked_sites, response_code = Rank.rank(zip_code, search_radius, comparator_weights, launch)

    if response_code != 200:
        return jsonify({"error": ranked_sites}), response_code
    
    ranked_sites_json = [site.to_json() for site in ranked_sites]
    response = {
        "ranked_sites": ranked_sites_json,
        "launch": launch,
        "search_radius": search_radius,
        "zip_code": zip_code
    }, 200

    return response
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
