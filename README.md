# LIFT-back

## Project Description

LIFT-back is the backend service for the LIFT project, designed to support launch site selection and ranking for model rocket launched. It provides APIs for retrieving weather forecasts, historical weather data, and ranking launch sites based on user-defined criteria such as distance, weather conditions, and site attributes. The backend is built with Flask (Python) for API endpoints and Node.js/Express for launch and site management, and integrates with external weather APIs ([NOAA](https://www.noaa.gov/)).

## Dependencies

### Python

- Flask
- flask_cors
- python-dotenv
- numpy

### Node.js

- express
- cors

## How to Install

### Python Backend

1. Clone the repository.
2. Navigate to the backend directory:

   ```bash
   cd LIFT-back
   ```

3. Install Python dependencies:

   ```bash
   pip install flask flask_cors python-dotenv numpy
   ```

### Node.js Backend

1. Install Node.js dependencies:

   ```bash
   npm install express cors
   ```

## How to Run

### Python Flask API

1. Ensure you have a `.env` file with necessary API keys (e.g., `NOAA_API_KEY`).
2. Start the Flask server:

   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000/`.

### Node.js Express Server

1. Start the Node.js server:

   ```bash
   npm start
   ```

   The server will run on `http://localhost:3000/`.

## Credits

LIFT was developed for the course CS 330: Intro to Software Engineering at West Virginia University. It is the result of a semester-long group project with 7 collaborators. The team was instructed in the Agile methodology and continued to scrum three times a week until the end of development.

### LIFT Roster

- Shelby Hansen, manager
- Lucian Baumgartner, product owner
- Bryson Herron, front end dev
- Michael Kaulfuss, scrum master
- Rex Mcallister, subject matter expert
- Greyson Meares, back end dev
- Noah Yoak, reviewer

The LIFT team wishes you clear skies and safe flights!
