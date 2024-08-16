# main.py

# dependencies
from dotenv import load_dotenv

# data handler
from data_handler.mongodb import mongoHandler, mongoURI
from data_handler.document_composer import documentComposer
from data_handler.group_updater import groupUpdater

# helpers
from helpers.age_check import ageCheck
from helpers.logger import log
from config import get_mongo_handler


def main():
    # Load environment variables from .env file
    load_dotenv()
    log("info", f"--------------------------------------------------------------")

    mongo_handler = get_mongo_handler()
    # update the groups that require it
    groups = mongo_handler.get_groups()

    for i, group in enumerate(groups):

        if group["group_enabled"] and ageCheck(group["refresh_time_unix"], group["refresh_rate"]):
            log(
                "info",
                f"[{i+1}] Fetching data for group: {group['group_name']}",
            )
            groups_request = {
                "latitude": group["location_latitude"],
                "longitude": group["location_longitude"],
            }

            # Fetch and update the group data
            groupUpdater(
                groups_request, group["group_id"], group["group_name"], mongo_handler
            )

    # Get locations to fetch data for
    locations = mongo_handler.get_locations()
    # Create a dictionary that maps group_id to group
    group_map = {group["group_number"]: group for group in groups}

    # Iterate through all the locations and gather data
    for i, location in enumerate(locations):
        log("info", ">>")

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

            # Look up the group using the group_id in the location
            group = group_map.get(location["location_group"])

            # Debugging output
            log("info", f"Location group: {location['location_group']}")

            location_request = {
                "location": {
                    "id": location["location_id"],
                    "name": location["location_name"],
                    "group": group,  # Add the group to the request
                    "latitude": location["location_latitude"],
                    "longitude": location["location_longitude"],
                },
                "currents": {
                    "latitude": location["currents_latitude"],
                    "longitude": location["currents_longitude"],
                },
            }

            # Use the documentComposer object, which precesses the data and prepares it for storage
            new_sample = documentComposer(location_request)

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
