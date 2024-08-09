# meteo_data
 Application that handles the gathering, processing and storing of meteo data for specified locations. It works with MongoDB Atlas as a database, and it's written mostly in python. The goal is to have it prepare data for many APIs to work on.

## Units and measurements

### Sample info:

* **location_id**: Int with unique location ID, so we don't have to use the document ID.

* **location_name**: String with the name of the place being sampled.

* **fetched_spanish_time**: String with daylight savings corrected time YYYY-MM-DD HH:MM:SS:MSMSMS+GMTOFFSET.

* **fetched_unix_time**: int with unix time indicating the time when that data was fetched.

* **sample_time**: string indicating the time of day that sample describes.

* **is_day**: bool indicating if that sample was taken during the day or at night

### Sea info:

* **wave_direction**: int (0-359) indicating the direction of the waves (0 is north).

* **wind_wave_direction**: int (0-359) indicating the direction of the waves caused by the wind (0 is north).

* **swell_wave_direction**: int (0-359) indicating the direction of the swell waves (0 is north).

* **ocean_current_direction**: int (0-359) indicating the direction of the ocean currents in that location (0 is north). This measurement is taken from a location close by, that has ocean currents information.

* **ocean_current_velocity**: float (m/s) indicating the speed of the ocean currents in that location. This measurement is taken from a location close by, that has ocean currents information.

### Weather info:

* **daily_data**: object containing data that summerizes a daily data point.

    * **sunrise**: string time of sunrise (2024-08-09T06:53)

    * **sunset**: string time of sunset (2024-08-09T06:53)

    * **sunlight**: float indicating how long the sun shined today. Cloudy counts as not shining i think.

    * **precipitation_total**: int Sum of all the precipitation types on this day.

    * **wind_main_direction**: int (0-359) Dominant wind direction for this day.


* **air_temperature**: float (ºC) indicating the air temperature.

* **air_humidity**: int (%) indicating the air humidity.

* **cloud_cover**: int (%) indicating the cloud cover at that location.

* **wind_speed**: float (m/s) indicating the wind speed at the ground for that location.

* **uv_index**: float (0-10) indicating the UV index for each hour