from data_logger import logger
from easyflie import easyflie
from pid_control import control
from raspberry_socketreader import viconUDP
from threading import Thread
import json
import time

# Constantly load setpoint from file
def thread_setpoint_loader():
    global setpoint,running
    while running:
        try: setpoint = json.load(open("dev-tools/const_setpoint.json"))
        except FileNotFoundError: setpoint = json.load(open("const_setpoint.json"))
        time.sleep(0.5)

# Main program / control loop
def thread_main_loop():
    global setpoint,running
    while running:
        # Get vicon data and log it
        vicon_data = vicon_udp.getTimestampedData() # fetch vicon data
        vicon_log.log_data(vicon_data) # save data with timestamp
        vicon_data.pop(0) # remove timestamp from dataset

        # Calculate error in position
        x_error = setpoint.get('x')-vicon_data[0]/1000
        y_error = setpoint.get('y')-vicon_data[1]/1000
        z_error = setpoint.get('z')-vicon_data[2]/1000
        
        # Get updated control from PID
        thrust = pid_thrust.update(z_error) + hover_thrust
        pitch = pid_pitch.update(x_error)
        roll = pid_roll.update(y_error)
        yaw = pid_yaw.update(None) #?

        # Send updated control params
        cf.send_setpoint(roll,pitch,yaw,thrust)
        time.sleep(1/(2*vicon_freq)) # allows other threads to run
        
if __name__ == '__main__':

    # constans
    hover_thrust = 41323
    drone_mass = 0.0318 # kilograms
    gravity = 9.81 # m/s²
    grav_force = drone_mass*gravity
    vicon_freq = 100

    # Setup vicon udp reader and logger
    vicon_udp = viconUDP()
    vicon_log = logger("vicon_log")
     
    # setup crazyFlie client
    cf = easyflie()
    cf.send_start_setpoint()

    # Setup PID control for all axes
    pid_thrust = control.PID(Kp=5000)
    pid_pitch = control.PID(0)
    pid_roll = control.PID(0)
    pid_yaw = control.PID(0)

    PID = [pid_thrust,pid_pitch,pid_roll,pid_yaw]
    for pid in PID:
        pid.start()

    # Tells treads to keep running
    running = True

    # Start program threads
    loader = Thread(target=thread_setpoint_loader)
    loader.start()
    time.sleep(0.2)
    main = Thread(target=thread_main_loop)
    main.start()

    # Handle program exit correctly
    while 1 :
        try: time.sleep(0.2)
        except KeyboardInterrupt:
            vicon_log.save_file()
            print("1")
            cf.send_stop_setpoint()
            running = False
            exit("Exiting program")
