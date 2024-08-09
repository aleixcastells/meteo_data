import requests
import json


def currentCheck(latitude, longitude):
    url = (
        "https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={latitude}&longitude={longitude}&"
        "current=wave_direction,wind_wave_direction,swell_wave_direction,ocean_current_velocity,ocean_current_direction&"
        "hourly=wave_direction,wind_wave_direction,swell_wave_direction,ocean_current_velocity,ocean_current_direction&"
        "daily=wave_height_max,wave_direction_dominant,wind_wave_height_max,wind_wave_direction_dominant,swell_wave_height_max,swell_wave_direction_dominant&"
        "timezone=auto&wind_speed_unit=ms&past_days=7&forecast_days=3&models=best_match"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad HTTP status codes
        data = response.json()

        # Pretty print JSON data
        if data["hourly"]["ocean_current_velocity"][0] == None:
            print("NO OCEANIC CURRENTS DATA FOR THIS LOCATION")
        else:
            print(data["hourly"]["ocean_current_velocity"])

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
