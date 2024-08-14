from dotenv import load_dotenv
import os
from data_handler.mongodb import mongoHandler


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

MONGO_URI_USR = os.getenv("MONGO_URI_USR")
MONGO_URI_PWD = os.getenv("MONGO_URI_PWD")
MONGO_URI_CLUSTER = os.getenv("MONGO_URI_CLUSTER")
MONGO_URI = f"mongodb+srv://{MONGO_URI_USR}:{MONGO_URI_PWD}@cluster0.jdmwldh.mongodb.net/?retryWrites=true&w=majority&appName={MONGO_URI_CLUSTER}"


database_name = "meteo_data"
locations_collection_name = "locations"
samples_collection_name = "samples"


# Initialize MongoDB handler
def get_mongo_handler():
    return mongoHandler(
        MONGO_URI,
        database_name,
        locations_collection_name,
        samples_collection_name,
    )


def get_next_location_id():
    # Fetch all locations from the database
    mongo_handler = get_mongo_handler()

    locations = mongo_handler.get_locations()

    if not locations:
        # If there are no locations, start with the first ID
        return 1000000

    # Extract all location_ids
    location_ids = [location["location_id"] for location in locations]

    # Find the maximum location_id
    max_location_id = max(location_ids)

    # Return the next location_id by incrementing the max
    return max_location_id + 1
