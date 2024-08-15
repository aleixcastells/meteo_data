# groupUpdater.py

# dependencies
import pytz
from datetime import datetime

# files
from api_handler.stormglass import StormGlass
from helpers.logger import log

spain_timezone = pytz.timezone("Europe/Madrid")
spain_time = datetime.now(spain_timezone)


def groupUpdater(request, group_id, group_name, mongo_handler):

    # Pre fectch the required APIs
    stormglass = StormGlass(request)

    update_request = {
        "water_temperature": stormglass.get_water_temperature(),
    }
    mongo_handler.update_group(group_id, update_request)
    log(
        "info",
        f"Updated group '{group_name}' with water surface temperature: {update_request['water_temperature']}°C",
    )

    return {
        "group_id": group_id,
        "water_temperature": update_request["water_temperature"],
    }
