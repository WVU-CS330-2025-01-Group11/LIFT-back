class Period:
    def __init__(self,
                  date,
                  percip,
                  short_forecast,
                  temperature,
                  wind_speed,
                  wind_direction):
        self.date = date
        self.percip = percip
        self.short_forecast = short_forecast
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

class ForecastData:
    def __init__(self, zip_code):
        self.zip_code = zip_code
        self.elevation = 0
        self.latitude = 0
        self.longitude = 0

        self.forecast_periods = []