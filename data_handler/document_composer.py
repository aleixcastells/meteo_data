# document_composer.py

# dependencies
import json
import time
import pytz
from datetime import datetime

# files
from helpers.logger import log
from api_handler.openmeteo import OpenMeteo

spain_timezone = pytz.timezone("Europe/Madrid")
spain_time = datetime.now(spain_timezone)
h_samples_history = 72


def documentComposer(request):

    # Pre fectch the required APIs
    open_meteo = OpenMeteo(request)

    document = {
        "location_id": request["location"]["id"],
        "location_name": request["location"]["name"],
        "fetched_spanish_time": spain_time.isoformat(),
        "fetched_unix_time": int(time.time()),  # Get current Unix timestamp
        "daily_data": {
            "sunrise": open_meteo.get_d_sunrise(),
            "sunset": open_meteo.get_d_sunset(),
            "sunlight": open_meteo.get_d_sunlight(),
            "precipitation_total": open_meteo.get_d_precipitation_total(),
            "wind_main_direction": open_meteo.get_d_wind_main_direction(),
            "water_surface_temperature": request["location"]["group"][
                "water_surface_temperature"
            ],
            "water_salinity": request["location"]["group"]["water_salinity"],
        },
        "hourly_data": {},
    }

    for i in range(h_samples_history):
        label = f"H{i}"
        document["hourly_data"][label] = {
            "sample_time": open_meteo.get_h_sample_time(i),
            "wave_direction": open_meteo.get_h_wave_direction(i),
            "wind_wave_direction": open_meteo.get_h_wind_wave_direction(i),
            "swell_wave_direction": open_meteo.get_h_swell_wave_direction(i),
            "ocean_current_direction": open_meteo.get_h_ocean_current_direction(i),
            "ocean_current_velocity": open_meteo.get_h_ocean_current_velocity(i),
            "air_temperature": open_meteo.get_h_air_temperature(i),
            "air_humidity": open_meteo.get_h_air_humidity(i),
            "cloud_cover": open_meteo.get_h_cloud_cover(i),
            "wind_speed": open_meteo.get_h_wind_speed(i),
            "uv_index": open_meteo.get_h_uv_index(i),
            "is_day": open_meteo.get_h_uv_index(i),
        }

    log("info", "Sample processed and cleaned")
    return document
