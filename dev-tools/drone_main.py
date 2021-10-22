from data_logger import logger
from easyflie import easyflie
from pid_control import control
from raspberry_socketreader import viconUDP
from threading import Thread
import json
import time

# Constantly load setpoint from file
def thread_setpoint_loader():
    global constant_setpoint,running
    constant_setpoint = {"x":0,"y":0,"z":0}
    while running:
        try: constant_setpoint = json.load(open("dev-tools/const_setpoint.json"))
        except FileNotFoundError: constant_setpoint = json.load(open("const_setpoint.json"))
        time.sleep(0.5)

# Main program / control loop
def thread_main_loop():
    global constant_setpoint,running
    while running:
        # Get vicon data and log it
        #vicon_data = vicon_udp.getTimestampedData() # fetch vicon data
        vicon_data = ["time",123,456,789,100,200,300]
        vicon_log.log_data(vicon_data) # save data with timestamp
        vicon_data.pop(0) # remove timestamp from dataset

        # Calculate error in position
        #x_error = setpoint[0]-vicon_data[0]
        #y_error = setpoint[1]-vicon_data[1]
        #z_error = setpoint[2]-vicon_data[2]
        z_error = constant_setpoint.get('z') #- vicon_data[2]

        # Get updated control from PID
        thrust = pid_thrust.update(z_error) + hover_thrust
        #pitch = pid_pitch.update(x_error)
        #roll = pid_roll.update(y_error)
        #yaw = pid_yaw.update(None) #?

        # Send updated control params
        #cf.send_setpoint(roll,pitch,yaw,thrust)
        time.sleep(0.1)
        

if __name__ == '__main__':

    # constans
    hover_thrust = 41323
    drone_mass = 0.0318 # kilograms
    gravity = 9.81 # m/s²
    grav_force = drone_mass*gravity

    # Setup vicon udp reader and logger
    vicon_udp = viconUDP()
    vicon_log = logger("vicon_log")
    vicon_log.log_data(["time","xpos","ypos","zpos","xrot","yrot","zrot"])

    # Initially all setpoints are constant
    setpoint = [-1000,1000,1000]

    # setup crazyFlie client
    cf = easyflie()
    #cf.send_start_setpoint()
    pitch, roll, yaw, thrust = 0,0,0,0

    # Setup PID control for all axes
    pid_thrust = control.PID(Kp=10)
    pid_pitch = control.PID(0)
    pid_roll = control.PID(0)
    pid_yaw = control.PID(0)

    PID = [pid_thrust,pid_pitch,pid_roll,pid_yaw]
    for pid in PID:
        pid.start()

    running = True

    loader = Thread(target=thread_setpoint_loader)
    loader.start()
    time.sleep(0.2)

    main = Thread(target=thread_main_loop)
    main.start()

    

    while 1 :
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            vicon_log.save_file()
            print("1")
            #cf.send_stop_setpoint()
            running = False
            exit("what")
