#!/bin/bash
# Raspberry Pi USB auto-detect + mount script

USER_NAME=$(whoami)
MOUNT_POINT="/home/$USER_NAME/usb"

echo "=== Raspberry Pi USB Auto‑Mount Script ==="
echo "Running as user: $USER_NAME"

echo ""
echo "Step 1: Ensuring mount point exists..."
sudo mkdir -p "$MOUNT_POINT"
sudo chown -R "$USER_NAME:$USER_NAME" "$MOUNT_POINT"
echo "Mount point ready at $MOUNT_POINT"

echo ""
echo "Step 2: Detecting USB storage device..."

# Find the first USB block device (e.g., sda, sdb, sdc)
USB_BLOCK=$(lsblk -o NAME,TRAN | awk '$2=="usb"{print $1; exit}')

if [ -z "$USB_BLOCK" ]; then
    echo "No USB storage device detected."
    echo "Check with: lsblk"
    exit 1
fi

echo "Detected USB device: /dev/$USB_BLOCK"

# Find the first partition on that device (e.g., sda1, sdb1)
USB_PART=$(lsblk -ln -o NAME "/dev/$USB_BLOCK" | awk 'NR==2{print $1}')

if [ -z "$USB_PART" ]; then
    echo "No partition found on /dev/$USB_BLOCK"
    echo "You may need to format the USB as FAT32."
    exit 1
fi

USB_PART="/dev/$USB_PART"
echo "Using partition: $USB_PART"

echo ""
echo "Step 3: Getting UUID for the USB partition..."
UUID=$(blkid -s UUID -o value "$USB_PART")

if [ -z "$UUID" ]; then
    echo "Could not read UUID. Check formatting of the USB drive."
    exit 1
fi

echo "USB UUID detected: $UUID"

echo ""
echo "Step 4: Mounting USB drive..."
sudo mount "$USB_PART" "$MOUNT_POINT" -o uid="$USER_NAME",gid="$USER_NAME"

if [ $? -eq 0 ]; then
    echo "USB mounted successfully at $MOUNT_POINT"
else
    echo "Mount failed. Check filesystem or try formatting the USB as FAT32."
    exit 1
fi

echo ""
echo "To unmount later, run:"
echo "    sudo umount $MOUNT_POINT"

echo ""
echo "=== Auto‑mount Setup Instructions ==="
echo "To enable auto‑mount on boot:"
echo "1. Edit fstab:"
echo "       sudo nano /etc/fstab"
echo "2. Add this line at the bottom:"
echo "       UUID=$UUID  $MOUNT_POINT  vfat  auto,nofail,noatime,users,rw,uid=$USER_NAME,gid=$USER_NAME  0  0"
echo ""
echo "Then reboot:"
echo "       sudo reboot"
echo ""
echo "USB will then auto‑mount at: $MOUNT_POINT"
echo "======================================"
