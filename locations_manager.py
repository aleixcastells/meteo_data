import os
import webbrowser
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from helpers.next_location_id import get_next_location_id
from helpers.currents_check import currentCheck
from helpers.logger import log
from config import get_mongo_handler


load_dotenv()

app = Flask(__name__)


mongo_handler = get_mongo_handler()

# Get locations to fetch data for
locations = mongo_handler.get_locations()


@app.route("/")
def index():
    log("info", "Opened location input HTML page")
    groups = mongo_handler.get_groups()  # Fetch the groups from MongoDB
    return render_template("location_input/index.html", groups=groups)


@app.route("/process_data", methods=["POST"])
def process_data():
    # Get the JSON data sent from the client
    data = request.get_json()

    # Extract data from the JSON object

    saved_data = {
        "enabled": data.get("location_enabled"),
        "name": data.get("location_name"),
        "group": data.get("location_group"),
        "location": {
            "longitude": data.get("location_longitude"),
            "latitude": data.get("location_latitude"),
        },
        "currents": {
            "longitude": data.get("currents_longitude"),
            "latitude": data.get("currents_latitude"),
        },
        "exposure_range": data.get("location_exposure_range"),
        "refresh_rate": data.get("refresh_rate"),
    }

    # Pass the data to your Python function
    result = dataProcess(saved_data)

    # Return the result as a JSON response
    return jsonify(result)  # Now it returns a properly JSON-serializable dictionary


@app.route("/check_currents", methods=["POST"])
def check_currents():
    # Get the JSON data sent from the client
    data = request.get_json()

    saved_data = {
        "location": {
            "longitude": data.get("location_longitude"),
            "latitude": data.get("location_latitude"),
        },
        "currents": {
            "longitude": data.get("currents_longitude"),
            "latitude": data.get("currents_latitude"),
        },
    }

    # Call the currentCheck function and get the result
    result = currentCheck(saved_data)

    # Return the result as a JSON response
    return jsonify({"result": result})


def dataProcess(saved_data):

    result = {
        "location_id": get_next_location_id(),
        "location_enabled": saved_data["enabled"],
        "location_name": saved_data["name"],
        "location_group": saved_data["group"],
        "location_longitude": saved_data["location"]["longitude"],
        "location_latitude": saved_data["location"]["latitude"],
        "currents_longitude": saved_data["currents"]["longitude"],
        "currents_latitude": saved_data["currents"]["latitude"],
        "location_exposure_range": saved_data["exposure_range"],
        "refresh_time_unix": 0,
        "refresh_rate": saved_data["refresh_rate"],
    }
    mongo_handler.addNewLocation(result)


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://localhost:5001/")

    app.run(debug=True, port=5001, host="0.0.0.0")
