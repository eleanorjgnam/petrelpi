from datetime import datetime, time
from dateutil import tz
from suntime import Sun, SunTimeException
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
video_config = picam2.configure(picam2.create_video_configuration(main={"size": (640,480)}))

RECORD_TIME = 30
SLEEP_TIME = 30

ST_JOHNS_LAT = 47.33
ST_JOHNS_LON = -52.42

def compute_times():
    sun = Sun(ST_JOHNS_LAT, ST_JOHNS_LON)
    time_zone = tz.gettz("America/St_Johns")
    global end, start
    end = sun.get_sunrise_time(at_date=datetime.now(), time_zone=time_zone).time()
    start = sun.get_sunset_time(at_date=datetime.now(), time_zone=time_zone).time()

compute_times()
camera_status_switch = start
recording = False

while True:
    current_time = datetime.now().time()

    if current_time >= start or current_time <= end: # check if current time is in recording time window
        if current_time >= camera_status_switch: # check if the camera status needs to be switch
            if recording: # has been recording.  shutdown the camera
                camera_status_switch = camera_status_switch + time(0, SLEEP_TIME)
                picam2.stop_recording()
            else: # was on standby, starts recording again
                camera_status_switch = camera_status_switch + time(0, RECORD_TIME)
                timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                filename = FfmpegOutput("/home/petrelpi/usb/{}.mp4".format(timestamp))
                encoder = H264Encoder(700_000,framerate=8)
                picam2.configure(video_config)
                picam2.set_controls({"FrameRate":8})
                picam2.start_recording(encoder,output=filename)

            recording = not recording
    else: # out of recording time window.  shutdown the camera
        if recording:
            picam2.stop_recording()

    if current_time >= time(0,0) and current_time < time(0, 1):
        compute_times()
