# openmeteo.py

# dependencies
import json

# files
from data_handler.fetch_api import fetchApi
from api_handler.api_usage import ApiUsage
from helpers.logger import log


class OpenMeteo:

    def __init__(
        self,
        request,
    ):
        self.request = request
        self.offset = 24 * 8
        self.api_usage = ApiUsage()

        if not self.api_usage.limit_reached("openmeteo", 3):
            self.fetch_api()  # Automatically fetch data when object is created
            log("info", "Sample retrieved from API")

        else:
            log("info", "Could not fetch")

    def fetch_api(self):

        self.currents_data = fetchApi(self.request["currents"], "marine")
        self.location_data = fetchApi(self.request["location"], "marine")
        self.weather_data = fetchApi(self.request["location"], "forecast")
        self.api_usage.record_call("openmeteo", 3)

    # daily methods

    def get_d_sunrise(self):
        return self.weather_data["daily"]["sunrise"][7]

    def get_d_sunset(self):
        return self.weather_data["daily"]["sunset"][7]

    def get_d_sunlight(self):
        return self.weather_data["daily"]["sunshine_duration"][7]

    def get_d_precipitation_total(self):
        return self.weather_data["daily"]["precipitation_sum"][7]

    def get_d_wind_main_direction(self):
        return self.weather_data["daily"]["wind_direction_10m_dominant"][7]

    # hourly methods

    def get_h_sample_time(self, index):
        return self.location_data["hourly"]["time"][self.offset - index]

    def get_h_wave_direction(self, index):
        return self.location_data["hourly"]["wave_direction"][self.offset - index]

    def get_h_wind_wave_direction(self, index):
        return self.location_data["hourly"]["wind_wave_direction"][self.offset - index]

    def get_h_swell_wave_direction(self, index):
        return self.location_data["hourly"]["swell_wave_direction"][self.offset - index]

    def get_h_ocean_current_direction(self, index):
        return self.currents_data["hourly"]["ocean_current_direction"][
            self.offset - index
        ]

    def get_h_ocean_current_velocity(self, index):
        return self.currents_data["hourly"]["ocean_current_velocity"][
            self.offset - index
        ]

    def get_h_air_temperature(self, index):
        return self.weather_data["hourly"]["temperature_2m"][self.offset - index]

    def get_h_air_humidity(self, index):
        return self.weather_data["hourly"]["relative_humidity_2m"][self.offset - index]

    def get_h_cloud_cover(self, index):
        return self.weather_data["hourly"]["cloud_cover"][self.offset - index]

    def get_h_wind_speed(self, index):
        return self.weather_data["hourly"]["wind_speed_10m"][self.offset - index]

    def get_h_uv_index(self, index):
        return self.weather_data["hourly"]["uv_index"][self.offset - index]

    def get_h_is_day(self, index):
        return (
            True
            if (self.weather_data["hourly"]["is_day"][self.offset - index])
            else False
        )
