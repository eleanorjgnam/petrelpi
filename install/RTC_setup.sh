#!/bin/bash
# Automated RTC setup script for DS1307 on Raspberry Pi

USER_NAME=$(whoami)

echo "=== Raspberry Pi RTC Setup Script (DS1307) ==="
echo "Running as user: $USER_NAME"
echo ""

###############################################
# 1. Test I2C detection
###############################################
echo "Step 1: Checking for I2C RTC at address 0x68..."
sudo i2cdetect -y 1

echo ""
echo "If you see '68', the RTC is detected."
echo "Continuing..."
sleep 2

###############################################
# 2. Add RTC overlay to /boot/config.txt
###############################################
CONFIG="/boot/config.txt"
OVERLAY="dtoverlay=i2c-rtc,ds1307"

echo "Step 2: Adding RTC overlay to $CONFIG..."

# Backup
sudo cp "$CONFIG" "$CONFIG.bak"

# Remove old entries
sudo sed -i "\|dtoverlay=i2c-rtc|d" "$CONFIG"

# Add new entry
echo "$OVERLAY" | sudo tee -a "$CONFIG" > /dev/null

echo "RTC overlay added."
echo ""

###############################################
# 3. Disable fake-hwclock
###############################################
echo "Step 3: Disabling fake-hwclock..."

sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock

echo "fake-hwclock disabled."
echo ""

###############################################
# 4. Modify /lib/udev/hwclock-set
###############################################
HWCLOCK_SET="/lib/udev/hwclock-set"

echo "Step 4: Updating $HWCLOCK_SET..."

# Backup
sudo cp "$HWCLOCK_SET" "$HWCLOCK_SET.bak"

# Comment out the systemd block
sudo sed -i 's/^if 

\[ -e \/run\/systemd\/system \]

 ; then/#if [ -e \/run\/systemd\/system ] ; then/' "$HWCLOCK_SET"
sudo sed -i 's/^    exit 0/#    exit 0/' "$HWCLOCK_SET"
sudo sed -i 's/^fi/#fi/' "$HWCLOCK_SET"

echo "hwclock-set updated."
echo ""

###############################################
# 5. Final instructions
###############################################
echo "=== RTC Setup Complete ==="
echo ""
echo "Now reboot the Raspberry Pi:"
echo "    sudo reboot"
echo ""
echo "After reboot, verify the RTC with:"
echo "    sudo i2cdetect -y 1   # should show 'UU'"
echo ""
echo "Check the current time:"
echo "    date"
echo ""
echo "To manually set the time:"
echo "    sudo date -s 'YYYY-MM-DD HH:MM:SS'"
echo ""
echo "Write time to hardware clock:"
echo "    sudo hwclock -w"
echo ""
echo "Read time from hardware clock:"
echo "    sudo hwclock -r"
echo ""
echo "==========================================="
