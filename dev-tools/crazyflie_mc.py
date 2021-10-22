import logging
import time

import cflib
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

debug_print = False

# Communication channel URI
URI = 'radio://0/80/2M'

cflib.crtp.init_drivers()

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':

    with SyncCrazyflie(URI) as scf:

        with MotionCommander(scf) as mc:

            mc.take_off()
            time.sleep(2)
            mc.up(1.5,0.1)
            mc.down(1.5,0.1)
            time.sleep(2)
            mc.land()

