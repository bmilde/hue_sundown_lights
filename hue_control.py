#!/usr/bin/env python3
"""
hue_control.py - A Python script to control Philips Hue lights.
"""

import argparse
import time
import random
import logging
import astral
import yaml
import os
from datetime import datetime, timezone, timedelta
from astral.sun import sun
from astral.geocoder import database, lookup

# Import the Hue and Light classes from your hue_snek module
from hue_snek import Hue, Light

# Constants
SECONDS_IN_A_DAY = 24.0 * 60.0 * 60.0
SECONDS_PER_HOUR = 60.0 * 60.0
DEFAULT_OFFSET = 25.0 * 60.0
DEFAULT_MIN_BRIGHTNESS = 10
DEFAULT_MAX_BRIGHTNESS = 100
DEFAULT_TRANSITION_INTERVAL = 3  # Default transition interval in seconds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hue_control.log'),
        logging.StreamHandler()
    ]
)

def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, config_path)

    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logging.info(f'Loaded configuration from {config_file}')
        return config
    except FileNotFoundError:
        logging.error(f'Config file not found: {config_file}')
        raise
    except yaml.YAMLError as e:
        logging.error(f'Error parsing config file: {e}')
        raise

def set_light_properties(hue, light_id, brightness, hue_value, saturation):
    """Set the properties of a light."""
    hue.set_light(light_id, 'on', 'true')
    hue.set_light(light_id, 'bri', str(brightness))
    hue.set_light(light_id, 'hue', str(hue_value))
    hue.set_light(light_id, 'sat', str(saturation))

def trigger_sunset(hue, min_brightness, max_brightness):
    """Trigger sunset mode, gradually increasing brightness."""
    logging.info('TURN THE LIGHT ON! :)')
    for brightness in range(min_brightness, max_brightness):
        for light_id in hue.get_lights('id'):
            light_name = hue.get_light(light_id, 'name')
            logging.info(f'Setting brightness for {light_name} to {brightness}')
            set_light_properties(hue, light_id, brightness, None, None)
            logging.debug(f'Current brightness: {hue.get_light(light_id, "bri")}')
        time.sleep(8)

def debug_all_on(hue, brightness=256):
    """Turn all lights on with a specified brightness."""
    for light_id in hue.get_lights('id'):
        light_name = hue.get_light(light_id, 'name')
        logging.info(f'Turning on {light_name} with brightness {brightness}')
        set_light_properties(hue, light_id, brightness, None, None)

def sunset_mode(hue, config, offset, min_brightness, max_brightness):
    """Sunset mode, gradually turning on lights as the sun sets."""
    sunset_trigger_active = False

    while True:
        if sunset_trigger_active:
            trigger_sunset(hue, min_brightness, max_brightness)
            sunset_trigger_active = False

        loc = config['location']
        city = astral.LocationInfo(loc['city'], loc['country'], loc['timezone'], loc['latitude'], loc['longitude'])
        logging.info((
            f"Information for {city.name}/{city.region}\n"
            f"Timezone: {city.timezone}\n"
            f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
        ))

        s = sun(city.observer, date=datetime.today())
        logging.info((
            f'Dawn:    {s["dawn"]}\n'
            f'Sunrise: {s["sunrise"]}\n'
            f'Noon:    {s["noon"]}\n'
            f'Sunset:  {s["sunset"]}\n'
            f'Dusk:    {s["dusk"]}\n'
        ))

        delta = s["sunset"] - datetime.now(timezone.utc) - timedelta(seconds=offset)
        delta_s = delta.total_seconds()

        if delta_s <= 0.0:
            logging.info(f'Last sunset trigger was: {abs(delta_s)} seconds ago')
            trigger_point = SECONDS_IN_A_DAY + delta_s
            logging.info(f'Next scheduled sunset trigger in: {trigger_point} seconds.')
        else:
            trigger_point = delta_s
            logging.info(f'Next scheduled sunset trigger in: {trigger_point} seconds.')

        if trigger_point > SECONDS_PER_HOUR:
            logging.info(f"Sleep for {SECONDS_PER_HOUR} seconds.")
            time.sleep(SECONDS_PER_HOUR)
        else:
            logging.info(f'Programming trigger, sleep for {trigger_point} seconds.')
            time.sleep(trigger_point)
            sunset_trigger_active = True

def turn_off_all(hue):
    """Turn off all lights."""
    for brightness in range(1):
        for light_id in hue.get_lights('id'):
            light_name = hue.get_light(light_id, 'name')
            logging.info(f'Turning off {light_name}')
            hue.set_light(light_id, 'on', 'false')
            hue.set_light(light_id, 'bri', str(brightness))
            logging.debug(f'Current brightness: {hue.get_light(light_id, "bri")}')
        time.sleep(10)

def turn_off_wohnzimmer(hue):
    """Turn off lights in the living room."""
    for brightness in range(1):
        for light_id in hue.get_lights('id'):
            name = hue.get_light(light_id, 'name')
            logging.info(f'Checking light: {name}')
            if "sofa" in name.lower() or "ess" in name.lower():
                logging.info(f'Turning off {name}')
                hue.set_light(light_id, 'on', 'false')
                hue.set_light(light_id, 'bri', str(brightness))
                logging.debug(f'Current brightness: {hue.get_light(light_id, "bri")}')
        time.sleep(10)

def turn_on_shell(hue, brightness):
    """Turn on specific lights with a specified brightness."""
    for light_id in hue.get_lights('id'):
        name = hue.get_light(light_id, 'name')
        logging.info(f'Checking light: {name}')
        if "muschel" in name.lower() or "kleine" in name.lower():
            logging.info(f'Turning on {name} with brightness {brightness}')
            set_light_properties(hue, light_id, brightness, None, None)
        time.sleep(10)

def turn_on_room(hue, filters, brightness):
    """Turn on lights matching the specified filters."""
    for light_id in hue.get_lights('id'):
        name = hue.get_light(light_id, 'name')
        logging.info(f'Checking light: {name}')
        if any(filter_str.lower() in name.lower() for filter_str in filters):
            logging.info(f'Turning on {name} with brightness {brightness}')
            set_light_properties(hue, light_id, brightness, None, None)

def turn_off_room(hue, filters):
    """Turn off lights matching the specified filters."""
    for light_id in hue.get_lights('id'):
        name = hue.get_light(light_id, 'name')
        logging.info(f'Checking light: {name}')
        if any(filter_str.lower() in name.lower() for filter_str in filters):
            logging.info(f'Turning off {name}')
            hue.set_light(light_id, 'on', 'false')
            hue.set_light(light_id, 'bri', '0')

def interpolate_color(color1, color2, factor):
    """Interpolate between two colors."""
    hue1, sat1 = color1
    hue2, sat2 = color2
    interpolated_hue = int(hue1 + (hue2 - hue1) * factor)
    interpolated_sat = int(sat1 + (sat2 - sat1) * factor)
    return interpolated_hue, interpolated_sat

def party_mode(hue, brightness, transition_interval):
    """Party mode, setting random colors to all lights and smoothly transitioning."""
    try:
        while True:
            # Set initial random colors
            color1 = {light_id: (random.randint(0, 65535), random.randint(0, 254)) for light_id in hue.get_lights('id')}
            color2 = {light_id: (random.randint(0, 65535), random.randint(0, 254)) for light_id in hue.get_lights('id')}

            # Set color1
            for light_id in hue.get_lights('id'):
                light_name = hue.get_light(light_id, 'name')
                current_hue, current_sat = color1[light_id]
                set_light_properties(hue, light_id, brightness, current_hue, current_sat)
                logging.info(f'Setting {light_name} to hue: {current_hue}, saturation: {current_sat}')
            time.sleep(1.5)

            # Set interpolated color
            for light_id in hue.get_lights('id'):
                light_name = hue.get_light(light_id, 'name')
                interpolated_color = interpolate_color(color1[light_id], color2[light_id], 0.5)
                current_hue, current_sat = interpolated_color
                set_light_properties(hue, light_id, brightness, current_hue, current_sat)
                logging.info(f'Setting {light_name} to interpolated hue: {current_hue}, saturation: {current_sat}')
            time.sleep(1.5)

            # Set color2
            for light_id in hue.get_lights('id'):
                light_name = hue.get_light(light_id, 'name')
                current_hue, current_sat = color2[light_id]
                set_light_properties(hue, light_id, brightness, current_hue, current_sat)
                logging.info(f'Setting {light_name} to hue: {current_hue}, saturation: {current_sat}')
            time.sleep(transition_interval)

    except KeyboardInterrupt:
        logging.info("Party mode stopped.")

def main():
    """Main function to parse arguments and control Hue lights."""
    parser = argparse.ArgumentParser(description='Control Philips Hue lights.')
    parser.add_argument('--mode', type=str, required=True,
                        choices=['sunset', 'turn_off_all', 'turn_off_wohnzimmer', 'turn_on_shell', 'party', 'turn_on_room', 'turn_off_room'],
                        help='Mode of operation')
    parser.add_argument('--brightness', type=int, default=110,
                        help='Brightness level for the lights (default: 110)')
    parser.add_argument('--min_brightness', type=int, default=DEFAULT_MIN_BRIGHTNESS,
                        help='Minimum brightness level for sunset mode (default: 10)')
    parser.add_argument('--max_brightness', type=int, default=DEFAULT_MAX_BRIGHTNESS,
                        help='Maximum brightness level for sunset mode (default: 100)')
    parser.add_argument('--offset', type=float, default=DEFAULT_OFFSET,
                        help='Offset in seconds for sunset mode (default: 1500.0)')
    parser.add_argument('--transition_interval', type=int, default=DEFAULT_TRANSITION_INTERVAL,
                        help='Transition interval in seconds for party mode (default: 3)')
    parser.add_argument('--room', type=str, default=None,
                        help='Room name (looks up filters from config.yaml)')
    parser.add_argument('--filters', type=str, default=None,
                        help='Comma-separated list of filter strings (overrides --room)')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to config file (default: config.yaml)')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Setup bridge from config
    hue_config = config['hue']
    hue = Hue(hue_config['bridge_ip'], hue_config['user_hash'])

    # Check the connection to the bridge
    ret = hue.checkup()
    if ret == 0:
        logging.info('Connected to hue!')

        # Handle room-based modes
        if args.mode in ['turn_on_room', 'turn_off_room']:
            # Determine filters
            if args.filters:
                filters = [f.strip() for f in args.filters.split(',')]
            elif args.room:
                if args.room not in config.get('rooms', {}):
                    logging.error(f'Room "{args.room}" not found in config')
                    return
                filters = config['rooms'][args.room]
            else:
                logging.error('Either --room or --filters must be specified for room-based modes')
                return

            if args.mode == 'turn_on_room':
                turn_on_room(hue, filters, args.brightness)
            elif args.mode == 'turn_off_room':
                turn_off_room(hue, filters)

        # Handle other modes
        elif args.mode == 'sunset':
            sunset_mode(hue, config, args.offset, args.min_brightness, args.max_brightness)
        elif args.mode == 'turn_off_all':
            turn_off_all(hue)
        elif args.mode == 'turn_off_wohnzimmer':
            turn_off_wohnzimmer(hue)
        elif args.mode == 'turn_on_shell':
            turn_on_shell(hue, args.brightness)
        elif args.mode == 'party':
            party_mode(hue, args.brightness, args.transition_interval)
    else:
        logging.error(f'Something went wrong: {ret}')

if __name__ == "__main__":
    main()

