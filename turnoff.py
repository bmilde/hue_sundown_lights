from hue_snek_pkg.hue_snek import Hue, Light
import time

def sunset(h):
    for brightness in range(1): 
        for light_id in h.get_lights('id'):
            print(h.get_light(light_id, 'name'))
#            ret = Light(light_id, h).set('bri', str(brightness))
            h.set_light(light_id, 'on', 'false')
            ret = h.set_light(light_id, 'bri', str(brightness))
            print(ret)
            print(h.get_light(light_id, 'bri'))
        time.sleep(10)

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
