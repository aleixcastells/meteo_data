from data_handler.mongodb import mongoHandler, mongoURI

# Define your database and collection names here
DATABASE_NAME = "meteo_data"
LOCATIONS_COLLECTION_NAME = "locations"
SAMPLES_COLLECTION_NAME = "samples"
GROUPS_COLLECTION_NAME = "groups"
API_USAGE_COLLECTION_NAME = "api_usage"


def get_mongo_handler():
    return mongoHandler(
        mongoURI(),
        DATABASE_NAME,
        LOCATIONS_COLLECTION_NAME,
        SAMPLES_COLLECTION_NAME,
        GROUPS_COLLECTION_NAME,
        API_USAGE_COLLECTION_NAME,
    )
