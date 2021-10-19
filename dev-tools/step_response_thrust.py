import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.utils.callbacks import Caller

URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Called when the link is established and the TOCs (that are not
# cached) have been downloaded
connected = Caller()

cflib.crtp.init_drivers(enable_debug_driver=False)

cf = Crazyflie()

cf.connected.add_callback(connected)
cf.open_link(URI)


cf.commander.send_setpoint(0,0,0,0)

for i in range(10):
    cf.commander.send_setpoint(0, 0, 0, 41323)
    print(i)
    time.sleep(0.2)

for i in range(10):
    cf.commander.send_setpoint(0, 0, 0, int(41323*0.9))
    print(i)
    time.sleep(0.2)

time.sleep(0.1)
cf.commander.send_stop_setpoint()
cf.close_link()