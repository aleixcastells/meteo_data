# mongodb.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from helpers.logger import log

from datetime import datetime

import time
from data_handler.fetch_api import fetchApi


class mongoHandler:
    def __init__(
        self, uri, db_name, locations_collection_name, samples_collection_name
    ):
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

    # Function to load the locations that have been added to the watchlist
    def get_locations(self):
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
                }
            },
        )
        log("info", "Location last refresh time updated")

    # Function to close the connection to Mongo
    def close(self):
        self.client.close()
