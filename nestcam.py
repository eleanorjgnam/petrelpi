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
import picamera

from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from time import sleep

R = 30 # 30s video. How long you want to record for
D = 10 # 10s delay. Delay between recording 



camera = PiCamera()

pir=MotionSensor(17) #17 = the output pin for the PIR sensor is GPIO 17 (pin 11)


while True:
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    filename = "/home/pi/usb/{}.h264".format(timestamp)
    
    pir.wait_for_motion()
    camera.start_preview()
    camera.start_recording(filename)
    print ("recording\n")
    sleep(R)
    #pir.wait_for_no_motion()
    camera.stop_recording()
    sleep(D)
    print ("idle\n")

#except KeyboardInterrupt:
 #   print ("Quit")
GPIO.cleanup()
