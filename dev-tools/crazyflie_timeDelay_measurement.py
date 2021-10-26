#This program is made to measure the timedelay between transmission of a command
#and recievement of the command

#This program sends a command from a Raspberry PI, once the command is sent a LED is turned on. 
#A LED on the crazyflie will light up everytime a new command is recieved. 
#A camera will be used to record the timing of the LED-turning on, and the LED on the crazyflie turning on

import cflib.crtp
import time
from cflib.crazyflie import Crazyflie
from gpiozero import LED

#Sets up the crazyflie API
# Define radio module URI
URI = 'radio://0/80/2M'

# Init USB drivers
cflib.crtp.init_drivers()

# Define CrazyFlie object
cf = Crazyflie()

# Apply URI to object
cf.open_link(URI)

# Initial values
roll = 0.0
pitch = 0.0
yaw = 0.0
thrust = 0.0
hover_thrust = 41323
prev_pitch = -1


#Sets up the LED
led = LED(17)

#Initialize the crzyflie
try:
    cf.commander.send_setpoint(0,0,0,0)
except Exception as e:
    print(e)
    exit()

#Wait two seconds
time.sleep(5)

#Send new command and turn on LED
led.on()
cf.commander.send_setpoint(0,0,0,1)#The drone should not be capable of flight with a thrust value of 1
time.sleep(5)
led.off()
cf.commander.send_stop_setpoint()
cf.close_link()