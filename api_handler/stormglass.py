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

        # record a 0 increment call to reset the function when necessary
        self.api_usage.record_call("stormglass", 0)
        self.api_usage.record_call("openmeteo", 0)

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
            self.bio_data["hours"] = self.bio_data["hours"][::-1]  # Reverse the order
            self.api_usage.record_call("stormglass", 1)

        except requests.exceptions.RequestException as e:
            log("error", f"Failed to fetch data from StormGlass API: {e}")
            self.weather_data = None
            self.bio_data = None

    def get_water_temperature(self):

        return buildSamplesArray(self.weather_data["hours"], "waterTemperature")

    def get_water_salinity(self):
        return buildSamplesArray(self.bio_data["hours"], "salinity")

    def get_water_chlorophyll(self):
        return buildSamplesArray(self.bio_data["hours"], "chlorophyll")

    def get_iron(self):
        return buildSamplesArray(self.bio_data["hours"], "iron")

    def get_water_nitrate(self):
        return buildSamplesArray(self.bio_data["hours"], "nitrate")

    def get_water_oxygen(self):
        return buildSamplesArray(self.bio_data["hours"], "oxygen")

    def get_water_ph(self):
        return buildSamplesArray(self.bio_data["hours"], "ph")

    def get_water_phosphate(self):
        return buildSamplesArray(self.bio_data["hours"], "phosphate")

    def get_water_phytoplankton(self):
        return buildSamplesArray(self.bio_data["hours"], "phyto")

    def get_water_silicate(self):
        return buildSamplesArray(self.bio_data["hours"], "silicate")

    def get_stormglass_time(self):
        return buildSamplesArray(self.bio_data["hours"], "time")


def buildSamplesArray(source, sample_name):
    try:
        max_value = None

        for sample in source:
            if isinstance(sample[sample_name], dict) and "sg" in sample[sample_name]:
                value = sample[sample_name]["sg"]
            else:
                value = sample[sample_name]

            if max_value is None or value > max_value:
                max_value = value  # Update max_value if the current value is greater

        return max_value

    except Exception as e:
        log("error", f"{sample_name} could not be read: {e}")
        return None
