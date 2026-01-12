#!/bin/bash
#
# Uninstall script for Hue Sunset Automation systemd service
# Run with: sudo ./uninstall-sunset-service.sh
#

set -e  # Exit on error

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run with sudo"
    echo "Usage: sudo ./uninstall-sunset-service.sh"
    exit 1
fi

SERVICE_NAME="hue-sunset.service"
SYSTEMD_DIR="/etc/systemd/system"

echo "========================================="
echo "Hue Sunset Automation - Service Uninstaller"
echo "========================================="
echo ""

# Stop service if running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping service..."
    systemctl stop "$SERVICE_NAME"
    echo "✓ Service stopped"
fi

# Disable service if enabled
if systemctl is-enabled --quiet "$SERVICE_NAME" 2>/dev/null; then
    echo "Disabling service..."
    systemctl disable "$SERVICE_NAME"
    echo "✓ Service disabled"
fi

# Remove service file
if [ -f "$SYSTEMD_DIR/$SERVICE_NAME" ]; then
    echo "Removing service file..."
    rm "$SYSTEMD_DIR/$SERVICE_NAME"
    echo "✓ Service file removed"
fi

# Reload systemd
systemctl daemon-reload
echo "✓ Systemd daemon reloaded"

echo ""
echo "========================================="
echo "Uninstallation complete!"
echo "========================================="
echo ""
