#"script for RaspPi terminal_RTC.py" script script FOR Research article for submission to Methods in Ecology and Evolution. 
#Hereward et al., Raspberry Pi nest cameras – an affordable tool for remote behavioural and conservation monitoring of bird nests.

#This script is from the following websites but easier to have in a file
#to copy script over to the raspberry pi terminal.

#Overview information: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/overview
#Setting up and testing I2C: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-up-and-test-i2c
#Set RTC: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

#In step 5 of the camera set up you should have already enabled the "I2C" by following through:
#pi -> Preferences -> Rasp.pi configuration –> interfaces –> enable…. Enable: ‘camera’, ‘SSH’ and ‘I2C’.

#We recommend using the preassembled DS1307 RTC Real Time Clock Module Board with additional GIPO pins.
#This is powered separately with a LiCB CR1220 3V Lithium Battery Button Cell Battery - this is
#important to install before scripting as this will then hold the corrected date and time even when
#the camera is switched off.


####Testing the I2C
#In raspberry pi terminal run the following line:
sudo i2cdetect -y 1 
#you should see ID #68 show up - that's the address of the DS1307, PCF8523 or DS3231 RTCs



####Setting up the RTC
#Run:
sudo nano /boot/config.txt 

#and then add this script at the end:
dtoverlay=i2c-rtc,ds1307

#save and sudo reboot
#then log back in and run:
sudo i2cdetect -y 1 #this should now show "UU" where "68" was before


#Next we need to disable the "fake hwclock" which interferes with the 'real' hwclock
#run the following lines one at a time:
    
    sudo apt-get -y remove fake-hwclock
    sudo update-rc.d -f fake-hwclock remove
    sudo systemctl disable fake-hwclock


#Now with the fake-hw clock off, you can start the original 'hardware clock' script.
#Run
sudo nano /lib/udev/hwclock-set

#and comment out these three lines (the lines after dev=$1):
#if [ -e /run/systemd/system ] ; then
# exit 0
#fi


#Finally check the actual time on the hardware by running
date

#Then to manually change the time open terminal and run the following script altering
#the date and time accordingly with 'YYYY-MM-DD HH:MM:SS'
sudo date -s '2017-02-05 15:30:00'

#Then check is it correct by re running
date

#Then write this as the definite time:
sudo hwclock -w to write the time 
#and one more check using the following script
sudo hwclock -r to read the time



