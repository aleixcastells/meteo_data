# age_check
import time


def ageCheck(last_update_time, threshold):
    age_delta = int(time.time()) - last_update_time
    age_hours = age_delta / 60 / 60
    return age_hours >= threshold
