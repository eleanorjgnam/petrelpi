
# no sensors needed, the camera turns on and records R min and then stops for D min

from picamera2 import Picamera2
from datetime import datetime, timedelta
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


R = 30 # 30min video. How long you want to record for
D = 10 # 10min delay. Delay between recording 

picam2 = Picamera2()
video_config=picam2.configure(picam2.create_video_configuration(main={"size": (640,480)}))

event_time = datetime.now() - timedelta(minutes=R)
recording = False

while True:
    current_time = datetime.now()

    # if the camera is not recording and it has been longer than the delay time since the last change
    if (current_time >= event_time + timedelta(minutes=D)) and not recording:
        recording = not recording
        event_time = datetime.now()

        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        filename = FfmpegOutput("/home/petrelpi/usb/{}.mp4".format(timestamp))
        encoder = H264Encoder(700_000,framerate=8)
    
        picam2.configure(video_config)
        picam2.set_controls({"FrameRate":8})
        picam2.start_recording(encoder,output=filename)
        print ("recording\n")

    # if the camera is recording for longer than the record time
    elif (current_time >= event_time + timedelta(minutes=R)) and recording:
        recording = not recording
        event_time = datetime.now()
        picam2.stop_recording()
        print ("idle\n")