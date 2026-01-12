#!/bin/bash
# Turn on shell lights with default brightness
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
python3 hue_control.py --mode turn_on_room --room shell --brightness 110
