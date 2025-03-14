from flask import Flask, jsonify, request
from APIClient import APIClient
# dotenv allows me to use my env file in this file
from dotenv import load_dotenv
# needed for env file as well
import os

#load environment variables from .env file
load_dotenv()

# initialize flask
app = Flask(__name__)

# initialize NOAA API client with API key
noaa_client= APIClient(api_key=os.getenv("NOAA_API_KEY"))

@app.route("/")
def home():
    return "Welcome to LIFT (BACKEND)"

@app.route("/api/wind-data", methods=["GET"])
def get_wind_data():
    """
    Endpoint to fetch wind data from the NOAA API.
    
    Query Parameters:
        locationId (str): The location ID (e.g., ZIP code or station ID).
        startDate (str): The start date in YYYY-MM-DD format.
        endDate (str): The end date in YYYY-MM-DD format.
    
    Returns:
        JSON: Wind data or an error message.
    """
    # Get query parameters from the request.
    location_id = request.args.get("locationId")
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")

    # Check if required parameters are missing.
    if not location_id or not start_date or not end_date:
        return jsonify({"error": "Missing parameters"}), 400  # Return a 400 Bad Request error.

    try:
        # Fetch wind data from the NOAA API.
        wind_data = noaa_client.fetch_wind_data(location_id, start_date, end_date)
        return jsonify(wind_data)  # Return the wind data as JSON.
    except Exception as e:
        # Handle errors (e.g., API request failed).
        return jsonify({"error": str(e)}), 500  # Return a 500 Internal Server Error.

# Run the Flask app.
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development.