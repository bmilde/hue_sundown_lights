#!/bin/bash
#
# Install script for Hue Sunset Automation systemd service
# Run with: sudo ./install-sunset-service.sh
#

set -e  # Exit on error

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run with sudo"
    echo "Usage: sudo ./install-sunset-service.sh"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/hue-sunset.service"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="hue-sunset.service"

echo "========================================="
echo "Hue Sunset Automation - Service Installer"
echo "========================================="
echo ""

# Check if service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "ERROR: Service file not found: $SERVICE_FILE"
    exit 1
fi

echo "Installing systemd service..."
echo "  Source: $SERVICE_FILE"
echo "  Destination: $SYSTEMD_DIR/$SERVICE_NAME"
echo ""

# Copy service file
cp "$SERVICE_FILE" "$SYSTEMD_DIR/$SERVICE_NAME"
echo "✓ Service file copied"

# Set permissions
chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME"
echo "✓ Permissions set"

# Reload systemd
systemctl daemon-reload
echo "✓ Systemd daemon reloaded"

# Enable service (auto-start on boot)
echo ""
read -p "Enable service to start on boot? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl enable "$SERVICE_NAME"
    echo "✓ Service enabled (will start on boot)"
else
    echo "○ Service not enabled (won't start on boot)"
fi

# Start service now
echo ""
read -p "Start service now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start "$SERVICE_NAME"
    echo "✓ Service started"
    echo ""
    echo "Checking service status..."
    sleep 1
    systemctl status "$SERVICE_NAME" --no-pager
else
    echo "○ Service not started"
fi

echo ""
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo ""
echo "Useful commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo "  Enable:  sudo systemctl enable $SERVICE_NAME"
echo "  Disable: sudo systemctl disable $SERVICE_NAME"
echo ""
echo "Log file: /home/me/hue_control/sunset.log"
echo ""
