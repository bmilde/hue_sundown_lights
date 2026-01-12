#!/bin/bash
# Start party mode with optional brightness parameter
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
BRIGHTNESS=${1:-110}
python3 hue_control.py --mode party --brightness "$BRIGHTNESS"
