#!/bin/bash
# Turn off extended living room lights
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
python3 hue_control.py --mode turn_off_room --room wohnzimmer2
