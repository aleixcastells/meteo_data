# openmeteo.py

# Here we use the OpenMeteo class to filter and process the response from fetchApi.
# We conform the data to our sample standards and prepare it for submission to the database.

# {
#     "location_id": 1000000,
#     "fetched_spanish_time": string (UTC Spain (CET/CEST): 2024-08-09T00:00) 2024-08-08T20:42:13.610837+02:00",
#     "fetched_unix_time": int 1723142534,
#     "T_0": {
#         "sample_time": string (UTC Spain (CET/CEST): 2024-08-09T00:00),
#         "wave_direction": int (0-359),
#         "wind_wave_direction": int (0-359),
#         "swell_wave_direction": int (0-359),
#         "ocean_current_direction": int (0-359),
#         "ocean_current_velocity": float (m/s),
#         "air_temperature": float
#         "air_humidity": int (0-100)
#         "cloud_cover": int
#         "wind_speed": float (m/s),
#         "uv_index": float
#         "is_day": false
#     },
# ...


import json
import time
import pytz

from data_handler.fetch_api import fetchApi
from datetime import datetime
from helpers.logger import log

spain_timezone = pytz.timezone("Europe/Madrid")
spain_time = datetime.now(spain_timezone)


class OpenMeteo:

    def __init__(
        self,
        location_id,
        location_name,
        location_latitude,
        location_longitude,
        currents_latitude,
        currents_longitude,
    ):
        self.location_id = location_id
        self.location_name = location_name
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.currents_latitude = currents_latitude
        self.currents_longitude = currents_longitude

    def fetch_weather(self):

        location_data = fetchApi(self.location_latitude, self.location_longitude, 1)
        currents_data = fetchApi(self.currents_latitude, self.currents_longitude, 1)
        weather_data = fetchApi(self.location_latitude, self.location_longitude, 2)
        log("info", "Sample retrieved from API")

        weather_data_raw = {
            "location_id": self.location_id,
            "location_name": self.location_name,
            "fetched_spanish_time": spain_time.isoformat(),
            "fetched_unix_time": int(time.time()),  # Get current Unix timestamp
            "daily_data": {
                "sunrise": weather_data["daily"]["sunrise"][3],
                "sunset": weather_data["daily"]["sunset"][3],
                "sunlight": weather_data["daily"]["sunshine_duration"][3],
                "precipitation_total": weather_data["daily"]["precipitation_sum"][3],
                "wind_main_direction": weather_data["daily"][
                    "wind_direction_10m_dominant"
                ][3],
                "precipitation_total": weather_data["daily"]["precipitation_sum"][3],
            },
        }

        time_intervals = [(0, "T_0")]

        # Generate intervals every 6 hours up to 72 hours ago
        for i in range(6, 73, 6):
            time_intervals.append((i, f"T_{i}"))

        # The last entry in the hourly list is assumed to be the most recent (current hour)
        last_index = len(location_data["hourly"]["time"]) - 48

        # Dynamically build the dictionary based on the defined intervals
        for hours_back, label in time_intervals:
            index = (
                last_index - hours_back
            )  # Calculate the index relative to the current time
            if index >= 0:  # Ensure the index is within bounds
                weather_data_raw[label] = {
                    "sample_time": location_data["hourly"]["time"][index],
                    "wave_direction": location_data["hourly"]["wave_direction"][index],
                    "wind_wave_direction": location_data["hourly"][
                        "wind_wave_direction"
                    ][index],
                    "swell_wave_direction": location_data["hourly"][
                        "swell_wave_direction"
                    ][index],
                    "ocean_current_direction": currents_data["hourly"][
                        "ocean_current_direction"
                    ][index],
                    "ocean_current_velocity": currents_data["hourly"][
                        "ocean_current_velocity"
                    ][index],
                    "air_temperature": weather_data["hourly"]["temperature_2m"][index],
                    "air_humidity": weather_data["hourly"]["relative_humidity_2m"][
                        index
                    ],
                    "cloud_cover": weather_data["hourly"]["cloud_cover"][index],
                    "wind_speed": weather_data["hourly"]["wind_speed_10m"][index],
                    "uv_index": weather_data["hourly"]["uv_index"][index],
                    "is_day": (
                        True if (weather_data["hourly"]["is_day"][index]) else False
                    ),
                }
            else:
                log("warn", f"No data available for {label}")

        # Print the result in JSON format for better readability
        weather_data_formatted = json.dumps(
            weather_data_raw, indent=4, ensure_ascii=False
        )
        log("info", "Sample processed and cleaned")
        return weather_data_raw
