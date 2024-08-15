# mongodb.py

# dependencies
import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# files
from helpers.logger import log


class mongoHandler:
    def __init__(
        self,
        uri,
        db_name,
        locations_collection_name,
        samples_collection_name,
        groups_collection_name,
        api_handler_collection_name,
    ):
        load_dotenv()

        try:
            self.client = MongoClient(uri)
            self.client.admin.command("ping")  # Check if the server is available
            log("info", "MongoDB connection established successfully.")

        except ConnectionFailure:
            log("error", "Failed to connect to MongoDB server.")
            raise

        self.db = self.client[db_name]
        self.locations_collection = self.db[locations_collection_name]
        self.samples_collection = self.db[samples_collection_name]
        self.groups_collection = self.db[groups_collection_name]
        self.api_handler_collection = self.db[api_handler_collection_name]

    # Function to load the locations that have been added to the watchlist
    def get_locations(self):
        log("info", "-")

        log("info", f"Using database: {self.db.name}")
        log("info", f"Using collection: {self.locations_collection.name}")

        try:
            locations_cursor = self.locations_collection.find()
            locations = list(locations_cursor)
            if not locations:
                log("warning", "No locations found in the collection.")
            else:
                log("info", f"Found {len(locations)} locations.")

            return locations

        except Exception as e:
            log("error", f"An error occurred while fetching locations: {e}")
            return []

    # Function to load the locations that have been added to the watchlist
    def get_groups(self):
        log("info", f"Using database: {self.db.name}")
        log("info", f"Using collection: {self.groups_collection.name}")

        try:
            groups_cursor = self.groups_collection.find()
            groups = list(groups_cursor)
            if not groups:
                log("warning", "No groups found in the collection.")
            else:
                log("info", f"Found {len(groups)} groups.")
            return groups
        except Exception as e:
            log("error", f"An error occurred while fetching groups: {e}")
            return []

    def get_api_usage(self):
        log("info", f"Using database: {self.db.name}")
        log("info", f"Using collection: {self.api_usage_collection.name}")

        try:
            api_usage_cursor = self.api_usage_collection.find()
            api_usage = list(api_usage_cursor)
            if not api_usage:
                log("warning", "No api_usage found in the collection.")
            else:
                log("info", f"Found {len(api_usage)} api_usage.")
            return api_usage
        except Exception as e:
            log("error", f"An error occurred while fetching api_usage: {e}")
            return []

    # Function to store the processed data
    def store_processed_data(self, data):
        self.samples_collection.insert_one(data)  # Directly insert the dictionary
        log("info", "Sample uploaded to database")

    # Function that changes the value of location["refresh_time_unix"] in the locations collection
    def updateLastRefeshTime(self, location_id):
        current_unix_time = int(time.time())  # Get current Unix timestamp

        self.locations_collection.update_one(
            {"location_id": location_id},
            {
                "$set": {
                    "refresh_time_unix": current_unix_time,
                    # "refresh_time_unix": 0,
                }
            },
        )
        log("info", "Location last refresh time updated")

    def addNewLocation(self, data):
        self.locations_collection.insert_one(data)
        log("info", "Location added to database")

    def update_group(self, group_id, request):

        result = self.groups_collection.update_one(
            {"group_id": group_id},
            {
                "$set": {
                    "water_surface_temperature": request["water_temperature"],
                    "water_salinity": request["water_salinity"],
                    "refresh_time_unix": int(time.time()),
                }
            },
        )
        if result.matched_count == 0:
            log("warning", f"No group found with group_id: {group_id}.")
        else:
            log(
                "info",
                f"Updated water_surface_temperature for group_id: {group_id}. Updated water_surface_temperature for group_id: {group_id}.",
            )

    # Function to close the connection to Mongo
    def close(self):
        self.client.close()


def mongoURI():
    # MongoDB connection details from environment variables
    MONGO_URI_USR = os.getenv("MONGO_URI_USR")
    MONGO_URI_PWD = os.getenv("MONGO_URI_PWD")
    MONGO_URI_CLUSTER = os.getenv("MONGO_URI_CLUSTER")
    MONGO_URI = f"mongodb+srv://{MONGO_URI_USR}:{MONGO_URI_PWD}@cluster0.jdmwldh.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_URI_CLUSTER}"
    return MONGO_URI
