#!/bin/bash
# Start sunset automation mode
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
"$SCRIPT_DIR/.venv/bin/python3" hue_control.py --mode sunset
