import requests
import json
import time

import time
from datetime import datetime, timezone


class OpenWeather:
    def __init__(self, latitude, longitude, api_key):
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_key

    def fetch_marine_weather(self):

        # Print Unix Timestamp
        unix_timestamp = int(time.time())  # Get current Unix timestamp
        print(f"Current Unix Timestamp: {unix_timestamp}")

        # Print UTC Time
        utc_time = datetime.now(timezone.utc)  # Get current time in UTC
        print(f"Current UTC Time: {utc_time.isoformat()}")
        url = (
            # "https://api.openweathermap.org/data/2.5/weather?"
            # f"lat={self.latitude}&lon={self.longitude}&"
            # f"appid={self.api_key}"
            "https://history.openweathermap.org/data/2.5/history/city?"
            f"lat={self.latitude}&lon={self.longitude}&"
            f"type=hour&start={unix_timestamp-604800}&end={unix_timestamp}&appid={self.api_key}"
        )

        print(url)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an error for bad HTTP status codes
            data = response.json()

            # Pretty print JSON data
            formatted_json = json.dumps(
                data, indent=4, sort_keys=True, ensure_ascii=False
            )
            print(formatted_json)
            return data

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
