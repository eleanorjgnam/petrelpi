#!/bin/bash
# Create and initialize the Python virtual environment
USER_NAME=$(whoami)
HOME_DIR="/home/$USER_NAME"
VENV_DIR="$HOME_DIR/birdcameravenv"
REQ_FILE="$HOME_DIR/petrelpi/install/requirements.txt"

echo "=== Bird Camera Virtual Environment Setup ==="
echo "Running as user: $USER_NAME"
echo ""

# Step 1: Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR ..."
    python3 -m venv --system-site-packages "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Step 2: Activate the environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 3: Install required packages
if [ -f "$REQ_FILE" ]; then
    echo "Installing requirements from $REQ_FILE ..."
    pip install -r "$REQ_FILE"
else
    echo "ERROR: Requirements file not found at $REQ_FILE"
    exit 1
fi

echo ""
echo "=== Virtual environment setup complete ==="
echo "To activate it later, run:"
echo "    source $VENV_DIR/bin/activate"
