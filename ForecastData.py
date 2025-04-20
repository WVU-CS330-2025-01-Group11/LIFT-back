import numpy as np

class Period:
    def __init__(self,
                  start,
                  end,
                  temp,
                  wind_low,
                  wind_high,
                  short_forecast,
                  percip_prob):
        self.start = start
        self.end = end
        self.percip_prob = percip_prob
        self.short_forecast = short_forecast
        self.temperature = temp
        self.wind_low = wind_low
        self.wind_high = wind_high

    def __str__(self):
        return f"Period(start={self.start}, end={self.end}, temperature={self.temperature}, wind_low={self.wind_low}, wind_high={self.wind_high}, short_forecast={self.short_forecast}, percip_prob={self.percip_prob})"

class ForecastData:
    def __init__(self, zip_code):
        self.zip_code = zip_code
        self.elevation = 0
        self.center_coords = np.zeros(2)
        self.polygon = np.array([])

        self.forecast_periods = []

    def __str__(self):
        string = f"ForecastData(zip_code={self.zip_code}, elevation={self.elevation}, center_coords={self.center_coords}, polygon={self.polygon}, forecast_periods=["
        for period in self.forecast_periods:
            string += str(period) + ", \n"
        string += "])"
        return string
    

    def from_dict(self, data):
        """
        Populate the ForecastData object from a dictionary.
        Args:
            data (dict): Dictionary containing forecast data.
        """
        geometry = data.get("geometry")
        poly_points = geometry.get("coordinates")[0]

        poly_list = []
        for point in poly_points:
            poly_list.append(np.array(point))

        self.polygon = np.array(poly_list)
        
        #compute the center of the polygon
        self.center_coords = np.mean(self.polygon, axis=0)

        self.elevation = data.get("properties").get("elevation").get("value")


        periods = data.get("properties").get("periods")
        for period in periods:
            # Only consider the day periods
            if period.get("isDaytime"):
                start_time = period.get("startTime")
                end_time = period.get("endTime")
                temp = period.get("temperature")
                wind_speed = period.get("windSpeed")

                if "to" in wind_speed:
                    wind_split = wind_speed.split(" to ")

                    wind_low = wind_split[0]
                    wind_high = wind_split[1].strip(" mph")

                    print (f"Wind low: {wind_low}, Wind high: {wind_high}")

                else:
                    wind_low = wind_speed.strip(" mph")
                    wind_high = wind_speed.strip(" mph")

                percip_prob = period.get("probabilityOfPrecipitation").get("value")
                if percip_prob is None:
                    percip_prob = 0.0
                else:
                    percip_prob = float(percip_prob)

                new_period = Period(
                    start_time,
                    end_time,
                    float(temp),
                    float(wind_low),
                    float(wind_high),
                    period.get("shortForecast"),
                    float(percip_prob)
                )
                self.forecast_periods.append(new_period)





        