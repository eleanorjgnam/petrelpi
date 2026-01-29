#"nestcam.py" script for script FOR Research article for submission to Methods in Ecology and Evolution. 
#Hereward et al., Raspberry Pi nest cameras – an affordable tool for remote behavioural and conservation monitoring of bird nests.

#This script combines the camera and the PIR sensor using a loop.
#Once there is motion this sets off the loop to record and delay
#as programmed in the script below.

#Connect the PIR sensor ‘VCC’ pin to the Real Time Clock ‘5V’ pin,
#and then connect the two ‘GND’ pins together,
#finally connect the PIR ‘OUT’ pin to the GPIO17 (pin 11) on the Pi-Zero board.

#Each created file is set to be named with the date and time and
#the files are set to be stored on the USB which you should already have 'mounted'
#using other scripts provided.



import RPi.GPIO as GPIO
import time
import picamera2

from gpiozero import MotionSensor
from picamera2 import Picamera2
from datetime import datetime
from time import sleep
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


R = 10 # 30s video. How long you want to record for
D = 10 # 10s delay. Delay between recording 



picam2 = Picamera2()
video_config=picam2.configure(picam2.create_video_configuration(main={"size": (640,480)}))

pir=MotionSensor(17) #17 = the output pin for the PIR sensor is GPIO 17 (pin 11)


while True:
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    filename = FfmpegOutput("/home/petrelpi/usb/{}.mp4".format(timestamp))
    encoder = H264Encoder(700_000,framerate=8)
    
    pir.wait_for_motion()
    #picam2.start_preview()
    picam2.configure(video_config)
    picam2.set_controls({"FrameRate":8})
    picam2.start_recording(encoder,output=filename)
    print ("recording\n")
    sleep(10)
    #pir.wait_for_no_motion()
    picam2.stop_recording()
    print ("idle\n")
    sleep(10)
    

#except KeyboardInterrupt:
 #   print ("Quit")
GPIO.cleanup()
