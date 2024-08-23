from hue_snek_pkg.hue_snek import Hue, Light
import time
import astral
from datetime import datetime, timezone, timedelta
from astral.sun import sun
from astral.geocoder import database, lookup

seconds_in_a_day = 24.0 * 60.0 * 60.0

seconds_per_hour = 60.0 * 60.0
offset = 25.0 * 60.0

def trigger_sunset(h):
    print('TURN THE LIGHT ON! :)')
    for brightness in range(10,200): 
        for light_id in h.get_lights('id'):
            print(h.get_light(light_id, 'name'))
#            ret = Light(light_id, h).set('bri', str(brightness))
            h.set_light(light_id, 'on', 'true')
            ret = h.set_light(light_id, 'bri', str(brightness))
            print(ret)
            print(h.get_light(light_id, 'bri'))
        time.sleep(8)

def debug_all_on(brightness=256):
    for light_id in h.get_lights('id'):
        h.set_light(light_id, 'on', 'true')
        ret = h.set_light(light_id, 'bri', str(brightness))

def sunset(h):

    sunset_trigger_active = False

    while True:
        if sunset_trigger_active:
            trigger_sunset(h)
            sunset_trigger_active = False
        #    city = lookup("Hamburg", database())i
        # Hamubrg: 53.551086, 9.993682
        # Frankfurt 50.11552000, 8.68417000

        city = astral.LocationInfo("Frankfurt am Main", "Germany", "Europe/Berlin", 50.11552000, 8.68417000)
        print((
        f"Information for {city.name}/{city.region}\n"
        f"Timezone: {city.timezone}\n"
        f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
        ))
        
        s = sun(city.observer, date=datetime.today())
        print((
        f'Dawn:    {s["dawn"]}\n'
        f'Sunrise: {s["sunrise"]}\n'
        f'Noon:    {s["noon"]}\n'
        f'Sunset:  {s["sunset"]}\n'
        f'Dusk:    {s["dusk"]}\n'
        ))

        delta = s["sunset"] - datetime.now(timezone.utc) - timedelta(seconds=offset)

        delta_s = delta.total_seconds()

        if(delta_s <= 0.0):
            print('Last sunset trigger was:', abs(delta_s), 'seconds ago')
            trigger_point = seconds_in_a_day + delta_s
            print('Next scheduld sunset trigger in:', trigger_point, 'seconds.')
        else:
            trigger_point = delta_s
            print('Next scheduld sunset trigger in:', trigger_point, 'seconds.')
        
        if trigger_point > seconds_per_hour:
            print("Sleep for", seconds_per_hour,'seconds.')
            time.sleep(seconds_per_hour)
        else:
            print('Programming trigger, sleep for', trigger_point, 'seconds.')
            time.sleep(trigger_point)
            sunset_trigger_active = True

    #print(delta.total_seconds())
    #print(s["sunset"] - datetime.now(timezone.utc))

user = 'turtlemaster'
user_hash = '1kPwBL7ioc1WgXz020bqooSwgiRK-o36A-px5RDj'

#setup bridge
h = Hue('192.168.0.20', user_hash)

#to check the connection to the bridge use:
ret = h.checkup()                     #returns 0 if connection and username OK

if ret == 0:
    print('Connected to hue!')
    sunset(h)
else:
    print('Something went wrong:', ret)
