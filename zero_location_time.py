from config import get_mongo_handler
from data_handler.mongodb import mongoHandler, mongoURI

mongo_handler = get_mongo_handler()
locations = mongo_handler.get_locations()

for i, location in enumerate(locations):

    # Update the location timestamp (unix time)
    mongo_handler.zeroLastRefeshTime(location["location_id"])
