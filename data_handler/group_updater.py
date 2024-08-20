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
        "water_salinity": stormglass.get_water_salinity(),
        "water_chlorophyll": stormglass.get_water_chlorophyll(),
        "water_iron": stormglass.get_iron(),
        "water_nitrate": stormglass.get_water_nitrate(),
        "water_oxygen": stormglass.get_water_oxygen(),
        "water_ph": stormglass.get_water_ph(),
        "water_phosphate": stormglass.get_water_phosphate(),
        "water_phytoplankton": stormglass.get_water_phytoplankton(),
        "water_silicate": stormglass.get_water_silicate(),
        "time": stormglass.get_stormglass_time(),
    }
    mongo_handler.update_group(group_id, update_request)
    log(
        "info",
        f"Updated group '{group_name}' with water surface temperature: {update_request['water_temperature']}°C",
    )
    log(
        "info",
        f"Updated group '{group_name}' with water salinity: {update_request['water_salinity']}°C",
    )

    return {
        "group_id": group_id,
        "water_temperature": update_request["water_temperature"],
        "water_salinity": update_request["water_salinity"],
        "water_chlorophyll": update_request["water_chlorophyll"],
        "water_iron": update_request["water_iron"],
        "water_nitrate": update_request["water_nitrate"],
        "water_oxygen": update_request["water_oxygen"],
        "water_ph": update_request["water_ph"],
        "water_phosphate": update_request["water_phosphate"],
        "water_phytoplankton": update_request["water_phytoplankton"],
        "water_silicate": update_request["water_silicate"],
        "time": update_request["time"],
    }
