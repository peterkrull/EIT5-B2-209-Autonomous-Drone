import time
import cflib.crtp
from cflib.crazyflie import Crazyflie

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

# Try to send zero-command to initialize
try:
    cf.commander.send_setpoint(0,0,0,0)
except Exception as e:
    print(e)
    exit()

# Send setpoint every 0.2 seconds
for i in range(30):
    if i < 10:
        pitch = 0
    elif i < 20:
        pitch = 10
    elif i < 30:
        pitch = 0

    # Print pitch on change
    if pitch != prev_pitch:
        print(f"Pitch : {pitch}")
    prev_pitch = pitch

    # Send command
    cf.commander.send_setpoint(roll,pitch,yaw,hover_thrust)
    time.sleep(0.2)

cf.commander.send_stop_setpoint()
cf.close_link()