import requests
from data_handler.urls import URL
from helpers.logger import log


def fetchApi(latitude, longitude, url_selector):

    try:
        response = requests.get(URL(latitude, longitude, url_selector).openmeteo())
        response.raise_for_status()  # Raises an error for bad HTTP status codes
        data = response.json()
        log("info", f"Fetched URL {url_selector}")
        return data

    except requests.exceptions.RequestException as e:
        log("error", f"An error occurred: {e}")
        return None
