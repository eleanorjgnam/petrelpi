#"script for RaspPi terminal_runonbootpy" script script FOR Research article for submission to Methods in Ecology and Evolution. 
#Hereward et al., Raspberry Pi nest cameras – an affordable tool for remote behavioural and conservation monitoring of bird nests.

# add these two lines of script so that "shutdown.py" and "nestcam.py" start on boot
#(i.e. when the power is plugged in)
#both of these scripts should already be in the 'scripts' folder in home -> pi


#go to raspberry pi terminal and type in:
sudo nano /etc/rc.local

#scroll to the end and add these two lines to the end of the script but above "exit 0"
sudo usr/bin/python3 /home/pi/scripts/shutdown.py & #this is the shutdown script that uses the clicker

sudo usr/bin/python3 /home/pi/scripts/nestcam.py & #this is the camera script

exit 0

#control x to exit and y to save

#then reboot the raspberry pi using
sudo reboot
