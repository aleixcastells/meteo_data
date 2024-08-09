import os
from dotenv import load_dotenv
from data_handler.mongodb import mongoHandler
from api_handler.openmeteo import OpenMeteo
from helpers.age_check import ageCheck
from helpers.logger import log


def main():
    # Load environment variables from .env file
    load_dotenv()
    log("info", f"--------------------------")

    # MongoDB connection details from environment variables
    MONGO_URI = os.getenv("MONGO_URI")
    database_name = "meteo_data"
    locations_collection_name = "locations"
    samples_collection_name = "samples"

    # Initialize MongoDB handler
    mongo_handler = mongoHandler(
        MONGO_URI, database_name, locations_collection_name, samples_collection_name
    )

    # Get locations to fetch data for
    locations = mongo_handler.get_locations()

    for location in locations:
        log("info", "---")

        if location["location_enabled"] and ageCheck(
            location["refresh_time_unix"], location["refresh_rate"]
        ):
            log("info", f"Fetching data for location: {location['location_name']}")
            log(
                "info",
                f"{location['location_name']} => Lat: {location['location_latitude']}, Lon: {location['location_longitude']}",
            )

            new_sample = OpenMeteo(
                location["location_id"],
                location["location_name"],
                location["location_latitude"],
                location["location_longitude"],
                location["currents_latitude"],
                location["currents_longitude"],
            ).fetch_weather()

            # Optionally, store the weather data in MongoDB
            mongo_handler.store_processed_data(new_sample)

            # Optionally, update the location timestamp
            mongo_handler.updateLastRefeshTime(location["location_id"])

        log("info", ageCheck(location["refresh_time_unix"], location["refresh_rate"]))


if __name__ == "__main__":
    main()
