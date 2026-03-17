#!/bin/bash
# Automatically add shutdown.py to /etc/rc.local for autostart

USER_NAME=$(whoami)
SCRIPT_DIR="/home/$USER_NAME/petrelpi"
RC_LOCAL="/etc/rc.local"
SHUTDOWN_SCRIPT="$SCRIPT_DIR/shutdown.py"

echo "=== Configuring rc.local autostart ==="

# Create rc.local if missing
if [ ! -f "$RC_LOCAL" ]; then
    echo "rc.local not found — creating it now..."
    sudo bash -c "cat > $RC_LOCAL" <<EOF
#!/bin/bash
# rc.local - created automatically

exit 0
EOF
    sudo chmod +x "$RC_LOCAL"
fi

# Backup rc.local
sudo cp "$RC_LOCAL" "$RC_LOCAL.bak"
echo "Backup created at $RC_LOCAL.bak"

# Remove old entries to avoid duplicates
sudo sed -i "\|python3 $SHUTDOWN_SCRIPT|d" "$RC_LOCAL"

# Insert new entry above 'exit 0'
sudo sed -i "/^exit 0/i sudo /usr/bin/python3 $SHUTDOWN_SCRIPT &" "$RC_LOCAL"

echo "Autostart entry added successfully."

echo ""
echo "Reboot to test:"
echo "    sudo reboot"
echo ""
echo "=== Done ==="
