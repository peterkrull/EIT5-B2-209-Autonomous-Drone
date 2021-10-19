import time
import cflib.crtp
from cflib.crazyflie import Crazyflie

class easyflie:

    def __init__(self,URI):
        self.URI = 'radio://0/80/2M'
        cflib.crtp.init_drivers()
        self.cf = Crazyflie()
        
    def send_start_setpoint(self):
        self.cf.open_link(self.URI)
        self.cf.commander.send_setpoint(0,0,0,0)

    def send_setpoint(self, roll, pitch, yaw, thrust):
        self.cf.commander.send_setpoint(roll, pitch, yaw, thrust)

    def send_stop_setpoint(self):
        self.cf.commander.send_stop_setpoint()
        self.cf.close_link()