#!/bin/bash
# Turn off bedroom lights
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
"$SCRIPT_DIR/.venv/bin/python3" hue_control.py --mode turn_off_room --room schlafzimmer
