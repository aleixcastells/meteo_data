# main.py

import os
from dotenv import load_dotenv
from data_handler.mongodb import mongoHandler
from api_handler.openmeteo import OpenMeteo
from helpers.age_check import ageCheck
from helpers.logger import log
from data_handler.document_composer import documentComposer


def main():
    # Load environment variables from .env file
    load_dotenv()
    log("info", f"--------------------------------------------------------------")

    # MongoDB connection details from environment variables
    MONGO_URI_USR = os.getenv("MONGO_URI_USR")
    MONGO_URI_PWD = os.getenv("MONGO_URI_PWD")
    MONGO_URI_CLUSTER = os.getenv("MONGO_URI_CLUSTER")
    MONGO_URI = f"mongodb+srv://{MONGO_URI_USR}:{MONGO_URI_PWD}@cluster0.jdmwldh.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_URI_CLUSTER}"

    database_name = "meteo_data"
    locations_collection_name = "locations"
    samples_collection_name = "samples"

    # Initialize MongoDB handler
    mongo_handler = mongoHandler(
        MONGO_URI, database_name, locations_collection_name, samples_collection_name
    )

    # Get locations to fetch data for
    locations = mongo_handler.get_locations()

    # Iterate through all the locations and gather data
    for i, location in enumerate(locations):
        log("info", "---")

        # Checks if that location is enabled and if it's time to refresh it again
        if location["location_enabled"] and ageCheck(
            location["refresh_time_unix"], location["refresh_rate"]
        ):
            log(
                "info",
                f"[{i+1}] Fetching data for location: {location['location_name']}",
            )

            # Prepares the request data for this location
            # [location] is the place we want to analise
            # [currents] is a location nearby that has currents information available

            request = {
                "location": {
                    "id": location["location_id"],
                    "name": location["location_name"],
                    "latitude": location["location_latitude"],
                    "longitude": location["location_longitude"],
                },
                "currents": {
                    "latitude": location["currents_latitude"],
                    "longitude": location["currents_longitude"],
                },
            }

            # Use the documentComposer object, which precesses the data and prepares it for storage
            new_sample = documentComposer(request)

            # Store the weather data in MongoDB
            mongo_handler.store_processed_data(new_sample)

            # Update the location timestamp (unix time)
            mongo_handler.updateLastRefeshTime(location["location_id"])

        log(
            "info",
            f"Location ({location['location_name']}: {location['location_id']}) was sampled: {ageCheck(location['refresh_time_unix'], location['refresh_rate'])}",
        )


# only run if executed directly
if __name__ == "__main__":
    main()
