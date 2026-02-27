
# Test file I made to debug nighttime_cycle.py as it is recording up to midnight, but stops after.
# This file can be run on any computer and will leave a trace as to what happens during the night cycle

from suntime import Sun
from dateutil import tz
from datetime import datetime, time, timedelta

sun = Sun(47.33, -52.42)

time_zone = tz.gettz("America/St_Johns")

RECORD_TIME = 30
SLEEP_TIME = 30

ST_JOHNS_LAT = 47.33
ST_JOHNS_LON = -52.42

current_time = datetime.now(tz=tz.gettz("America/St_Johns"))

def compute_times():
    sun = Sun(ST_JOHNS_LAT, ST_JOHNS_LON)
    time_zone = tz.gettz("America/St_Johns")
    global end, start
    end = sun.get_sunrise_time(at_date=datetime.now(), time_zone=time_zone)
    start = sun.get_sunset_time(at_date=datetime.now(), time_zone=time_zone)
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    print(f"{timestamp}: compute start:{start} end:{end}")

compute_times()
camera_status_switch = start
recording = False

while True:
    current_time = datetime.now(tz=tz.gettz("America/St_Johns"))

    if current_time >= start or current_time <= end: # check if current time is in recording time window
        if current_time >= camera_status_switch: # check if the camera status needs to be switch
            if recording: # has been recording.  shutdown the camera
                camera_status_switch = camera_status_switch + timedelta(minutes=SLEEP_TIME)
                timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                print(f"{timestamp}: stop")
            else: # was on standby, starts recording again
                camera_status_switch = camera_status_switch + timedelta(minutes=RECORD_TIME)
                timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                print(f"{timestamp}: recording")
            recording = not recording
    else: # out of recording time window.  shutdown the camera
        if recording:
            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            print(f"{timestamp}: stop")

    if current_time.time() >= time(0,0) and current_time.time() < time(0, 1):
        compute_times()
