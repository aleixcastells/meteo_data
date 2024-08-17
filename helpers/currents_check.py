import requests
import json
from helpers.logger import log


def currentCheck(saved_data):
    url = (
        "https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={saved_data['currents']['latitude']}&longitude={saved_data['currents']['longitude']}&"
        "hourly=ocean_current_velocity,ocean_current_direction&"
        "timezone=auto&forecast_days=3&models=best_match"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad HTTP status codes
        data = response.json()

        if data["hourly"]["ocean_current_velocity"][0] == None:
            log(
                "info",
                f"DATA ERROR. {saved_data['currents']['latitude']}, {saved_data['currents']['longitude']} has no ocean information.",
            )
            return False
        else:
            log(
                "info",
                f"DATA FOUND. {saved_data['currents']['latitude']}, {saved_data['currents']['longitude']} is suitable as an ocean data gathering point",
            )
            return True

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
