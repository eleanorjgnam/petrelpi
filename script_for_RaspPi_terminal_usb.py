#"script for RaspPi terminal_usb.py" script script FOR Research article for submission to Methods in Ecology and Evolution. 
#Hereward et al., Raspberry Pi nest cameras – an affordable tool for remote behavioural and conservation monitoring of bird nests.

#Script created from: rasberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk
#With edits from co-author L Maggs

####Note that each USB has a unique code, it is possible to create several mount points and
####mount different USBs to different files but to keep things simple we recommend only using one USB
####per raspberry pi board to avoid confusion.


#Before starting the USB needs to be formatted (fat32)

#first need to find out the unique reference UUID code for the USB:
#open raspberry pi terminal and type in:
ls -l /dev/disk/by-uuid/
#the USB has /sda1 at the end.
#Make note of the blue highlighted combination.

#next you need to create a mount point - this is the folder that the USB will be 'mounted' to.
#We suggest using a USB as this allows for larger storage capacity (rather than the micro SD card/hard drive)

sudo mkdir /home/pi/usb #this you should have already done in step 6 of the instructions
sudo chown -R pi:pi /home/pi/usb #this makes sure the Pi user owns this folder


#next you manually mound the drive:
#this allows the user to read, write and delete files in the home/pi/usb folder
sudo mount /dev/sda1 /home/pi/usb -o uid=pi,gid=pi


####NOTE - need to make sure you shutdown pi everytime BEFORE removing the USB
#if you don't you can 'un mount' first using this script:
#umount /home/pi/usb  #the code is purposefully missing the 'n' of un



# to avoid having to remount the USB everytime you can make it run on boot = auto mount
#to do this you need the UUID code that you found earlier.

#Then run:
sudo nano /etc/fstab

#right at the end of the script add to following
UUID= *add code here* /home/pi/usb vfat auto,nofail,noatime,users,rw,uid=pi,gid=pi 0 0
#add the unique UUID code that you found earlier and therefore removing *add code here*

#Then reboot the raspberry pi board to make sure it has worked:
sudo reboot


#The USB should now be auto-mounted and avalible as "/home/pi/usb"
