# stormglass.py

# dependencies
import json
import arrow
import requests
import os
from dotenv import load_dotenv

# files
from helpers.logger import log
from api_handler.api_usage import ApiUsage


class StormGlass:
    def __init__(self, request_info):
        self.request_info = request_info
        self.weather_data = None  # This will hold the fetched data
        self.bio_data = None  # This will hold the fetched data
        self.api_usage = ApiUsage()  # Create an instance of ApiUsage

        if not self.api_usage.limit_reached("stormglass", 1):
            self.fetch_api()  # Automatically fetch data when the object is created

        log("info", "Sample retrieved from API")

    def fetch_api(self):
        load_dotenv()
        STORMGLASS_KEY_WEATHER = os.getenv("STORMGLASS_KEY_WEATHER")
        STORMGLASS_KEY_BIO = os.getenv("STORMGLASS_KEY_BIO")

        # Get first hour of today
        start = arrow.now().floor("day")
        # Get last hour of today
        end = arrow.now().ceil("day")

        try:
            weather_response = requests.get(
                "https://api.stormglass.io/v2/weather/point",
                params={
                    "lat": self.request_info["latitude"],
                    "lng": self.request_info["longitude"],
                    "params": ",".join(["waterTemperature"]),
                    "start": start.to("UTC").timestamp(),  # Convert to UTC timestamp
                    "end": end.to("UTC").timestamp(),  # Convert to UTC timestamp
                },
                headers={"Authorization": STORMGLASS_KEY_WEATHER},
            )
            weather_response.raise_for_status()  # Raise an error for bad responses

            self.weather_data = weather_response.json()  # Store the response JSON

            bio_response = requests.get(
                "https://api.stormglass.io/v2/bio/point",
                params={
                    "lat": self.request_info["latitude"],
                    "lng": self.request_info["longitude"],
                    "params": ",".join(
                        [
                            "chlorophyll",
                            "iron",
                            "nitrate",
                            "phyto",
                            "oxygen",
                            "ph",
                            "phytoplankton",
                            "phosphate",
                            "silicate",
                            "salinity",
                        ]
                    ),
                    "start": start.to("UTC").timestamp(),  # Convert to UTC timestamp
                    "end": end.to("UTC").timestamp(),  # Convert to UTC timestamp
                },
                headers={"Authorization": STORMGLASS_KEY_BIO},
            )
            bio_response.raise_for_status()  # Raise an error for bad responses

            self.bio_data = bio_response.json()  # Store the response JSON
            self.api_usage.record_call("stormglass", 1)

        except requests.exceptions.RequestException as e:
            log("error", f"Failed to fetch data from StormGlass API: {e}")
            self.weather_data = None
            self.bio_data = None

    # Example method to get water temperature
    def get_water_temperature(self):

        try:
            # Extract the first available water temperature data point
            water_surface_temperature = self.weather_data["hours"][0][
                "waterTemperature"
            ]["sg"]

            return water_surface_temperature

        except (KeyError, IndexError) as e:
            log("error", f"Error extracting water temperature: {e}")
            return None

        # Example method to get water temperature

    def get_water_salinity(self):

        try:
            # Extract the first available water temperature data point
            water_salinity = self.bio_data["hours"][0]["salinity"]["sg"]

            return water_salinity

        except (KeyError, IndexError) as e:
            log("error", f"Error extracting water salinity: {e}")
            return None
