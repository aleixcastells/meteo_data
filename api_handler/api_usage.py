# api_usage.py

# dependencies
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

# files
from helpers.logger import log
from data_handler.mongodb import mongoURI


class ApiUsage:
    def __init__(self):
        self.client = MongoClient(mongoURI())
        self.db = self.client["meteo_data"]
        self.collection = self.db["api_usage"]

    def limit_reached(self, api_name, margin):

        # Fetch the API usage document
        api_usage = self.collection.find_one({"api_name": api_name})
        log("info", f"reading from {api_name}")

        # Check if the daily limit has been reached
        if api_usage["api_calls_today"] >= api_usage["api_calls_today_max"] - margin:
            log("info", f"API call limit reached for {api_name}.")
            return True

        return False

    def record_call(self, api_name, amount):
        try:

            current_month = datetime.now().month
            current_day = datetime.now().day

            # Fetch the API usage document
            api_usage = self.collection.find_one({"api_name": api_name})

            if not api_usage:
                log("error", f"No API found for {api_name}")
                return

            # Check if it's a new month, reset the monthly count
            if api_usage["current_month"] != current_month:

                log(
                    "info",
                    f"({api_name}) Resetting monthly call count.",
                )
                self.collection.update_one(
                    {"api_name": api_name},
                    {
                        "$set": {
                            "api_calls_month": amount,
                            "current_month": current_month,
                            "api_calls_today": amount,
                        },
                        "$inc": {
                            "api_calls_ever": amount,
                        },
                    },
                )
            else:
                if api_usage["current_day"] != current_day:
                    log(
                        "info",
                        f"({api_name}) Resetting monthly API count.",
                    )
                    self.collection.update_one(
                        {"api_name": api_name},
                        {
                            "$set": {
                                "current_day": current_day,
                                "api_calls_today": amount,  # Reset today's call count
                            },
                            "$inc": {
                                "api_calls_ever": amount,
                            },
                        },
                    )

                else:
                    # Increment the daily and monthly counters
                    self.collection.update_one(
                        {"api_name": api_name},
                        {
                            "$inc": {
                                "api_calls_today": amount,
                                "api_calls_month": amount,
                                "api_calls_ever": amount,
                            }
                        },
                    )

        except Exception as e:
            log("error", f"An error occurred while recording API call: {e}")
