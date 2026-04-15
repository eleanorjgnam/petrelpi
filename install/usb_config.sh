#!/bin/bash
# Raspberry Pi USB auto-detect + auto-partition + auto-label + auto-mount script

USER_NAME=$(whoami)
MOUNT_POINT="/home/$USER_NAME/usb"
USB_LABEL="PETRELUSB"

echo "=== Raspberry Pi USB Auto‑Mount Script (LABEL-based) ==="
echo "Running as user: $USER_NAME"

echo ""
echo "Step 1: Ensuring mount point exists..."
sudo mkdir -p "$MOUNT_POINT"
sudo chown -R "$USER_NAME:$USER_NAME" "$MOUNT_POINT"
echo "Mount point ready at $MOUNT_POINT"

echo ""
echo "Step 2: Detecting USB storage device..."

USB_BLOCK=$(lsblk -o NAME,TRAN | awk '$2=="usb"{print $1; exit}')

if [ -z "$USB_BLOCK" ]; then
    echo "No USB storage device detected."
    echo "Check with: lsblk"
    exit 1
fi

echo "Detected USB device: /dev/$USB_BLOCK"

# Find the first partition on that device (e.g., sda1)
USB_PART=$(lsblk -ln -o NAME "/dev/$USB_BLOCK" | awk 'NR==2{print $1}')

echo ""
echo "Step 3: Checking for partitions..."

if [ -z "$USB_PART" ]; then
    echo "No partition found on /dev/$USB_BLOCK"
    echo "Creating new FAT32 partition..."

    sudo parted -s "/dev/$USB_BLOCK" mklabel msdos
    sudo parted -s "/dev/$USB_BLOCK" mkpart primary fat32 1MiB 100%

    sleep 2

    USB_PART="${USB_BLOCK}1"
    echo "Created partition: /dev/$USB_PART"

    echo "Formatting as FAT32..."
    sudo mkfs.vfat -F 32 "/dev/$USB_PART"
else
    echo "Using partition: /dev/$USB_PART"
fi

USB_PART="/dev/$USB_PART"

echo ""
echo "Step 4: Setting or verifying label..."

CURRENT_LABEL=$(blkid -s LABEL -o value "$USB_PART")

if [ "$CURRENT_LABEL" != "$USB_LABEL" ]; then
    echo "Setting label to $USB_LABEL"
    sudo fatlabel "$USB_PART" "$USB_LABEL"
else
    echo "USB already labeled as $USB_LABEL"
fi

echo ""
echo "Step 5: Mounting USB drive..."
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
echo "       LABEL=$USB_LABEL  $MOUNT_POINT  vfat  auto,nofail,noatime,users,rw,uid=$USER_NAME,gid=$USER_NAME  0  0"
echo ""
echo "Then reboot:"
echo "       sudo reboot"
echo ""
echo "USB will then auto‑mount at: $MOUNT_POINT"
echo "======================================"
