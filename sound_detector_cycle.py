import RPi.GPIO as GPIO

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from datetime import datetime, timedelta
from dateutil import tz

channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

picam2 = Picamera2()
video_config = picam2.configure(picam2.create_video_configuration(main={"size": (640,480)}))

TIME_ZONE = tz.gettz("America/St_Johns")
KEEP_LISTENING_FOR = timedelta(seconds=30)

sound_detected_flag = False
last_sound_detected = datetime.now(tz=TIME_ZONE) - KEEP_LISTENING_FOR
recording = False

def callback(channel):
    global sound_detected_flag, last_sound_detected
    sound_detected_flag = True
    last_sound_detected = datetime.now()


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
    if sound_detected_flag: #sound was detected
        if (last_sound_detected + KEEP_LISTENING_FOR) <= datetime.now(): # the last sound detected was a while ago
            sound_detected_flag = False
            recording = False
            picam2.stop_recording()
        else: # new sound, start recording
            if not recording: # was on standby, starts recording again
                timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                filename = FfmpegOutput("/home/petrelpi/usb/{}.mp4".format(timestamp))
                encoder = H264Encoder(700_000,framerate=8)
                picam2.configure(video_config)
                picam2.set_controls({"FrameRate":8})
                picam2.start_recording(encoder,output=filename)
                recording = True