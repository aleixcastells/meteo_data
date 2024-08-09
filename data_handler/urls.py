# URLs
from helpers.logger import log


class URL:
    def __init__(self, latitude, longitude, url_selector):
        self.latitude = latitude
        self.longitude = longitude
        self.url_selector = url_selector

    def openmeteo(self):
        url_marine = (
            "https://marine-api.open-meteo.com/v1/marine?"
            f"latitude={self.latitude}&longitude={self.longitude}&"
            "current=wave_direction,wind_wave_direction,swell_wave_direction,ocean_current_velocity,ocean_current_direction&"
            "hourly=wave_direction,wind_wave_direction,swell_wave_direction,ocean_current_velocity,ocean_current_direction&"
            "daily=wave_height_max,wave_direction_dominant,wind_wave_height_max,wind_wave_direction_dominant,swell_wave_height_max,swell_wave_direction_dominant&"
            "timezone=auto&wind_speed_unit=ms&past_days=7&forecast_days=3&models=best_match"
        )
        url_forecast = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&longitude={self.longitude}&"
            "hourly=temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m,uv_index,is_day&daily=sunrise,sunset,sunshine_duration,precipitation_sum,wind_direction_10m_dominant&"
            "timezone=auto&wind_speed_unit=ms&past_days=7&forecast_days=3&models=best_match"
        )

        if self.url_selector == 1:
            return url_marine

        if self.url_selector == 2:
            return url_forecast
