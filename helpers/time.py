from datetime import datetime
import pytz


def get_timestamp_today():

    spain_timezone = pytz.timezone("Europe/Madrid")
    spain_time = datetime.now(spain_timezone)

    day_number = spain_time.day
    day_zero = "" if day_number > 9 else "0"

    month_number = spain_time.month
    month_zero = "" if month_number > 9 else "0"

    year_number = spain_time.year

    return f"{year_number}-{month_zero}{month_number}-{day_zero}{day_number}"
