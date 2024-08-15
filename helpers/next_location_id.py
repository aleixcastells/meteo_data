from config import get_mongo_handler

mongo_handler = get_mongo_handler()


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
