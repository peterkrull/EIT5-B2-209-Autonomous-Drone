import json
import time

from threading import Thread
from math import pi,cos

from controllers import control
from data_logger import logger
from easyflie import easyflie
from raspberry_socketreader import viconUDP
from path_follow import PathFollow

# Enable logs
log = True
log_error = True
log_sp = True
log_cal = True
log_lim = True

# Constantly load setpoint from file
def thread_setpoint_loader():
    global sp,running
    while running:
        try: sp = json.load(open("dev-tools/const_setpoint.json"))
        except FileNotFoundError: sp = json.load(open("const_setpoint.json"))
        time.sleep(0.5)

def thread_setpoint_loader2():
    global sp,running,vicon_data,path
    vicon_data = [0,0,0,0]
    while running:
        sp = path.getRef(vicon_data) 
        print(sp)
        time.sleep(0.1)

# Main program / control loop
def thread_main_loop():
    global sp,running,vicon_data

    # Add column title to log file
    if log : col_titles = ['time','x_pos','y_pos','z_pos','x_rot','y_rot','z_rot']              # LOG CLUSTER 1
    if log and log_error : col_titles += ['x_error','y_error','z_error','yaw_error']            # LOG CLUSTER 2
    if log and log_sp : col_titles += ['x_setpoint','y_setpoint','z_setpoint','yaw_setpoint']   # LOG CLUSTER 3
    if log and log_cal : col_titles += ['thrust_cal','pitch_cal','roll_cal','yaw_cal']          # LOG CLUSTER 4
    if log and log_lim : col_titles += ['thrust_lim','pitch_lim','roll_lim','yaw_lim']          # LOG CLUSTER 5
    if log : vicon_log.log_data(col_titles)
    if log : del col_titles

    while running:
        # Get vicon data and log it
        vicon_data = vicon_udp.getTimestampedData() # fetch vicon data
        if log : log_data = vicon_data # LOG CLUSTER 1

        # Check room limits
        sp['x'] = control.limiter(sp['x'],rl['x']['min'],rl['x']['max'])
        sp['y'] = control.limiter(sp['y'],rl['y']['min'],rl['y']['max'])
        sp['z'] = control.limiter(sp['z'],rl['z']['min'],rl['z']['max'])

        # Calculate error in position and yaw
        x_error = (sp.get('x')-vicon_data[1])/1000
        y_error = (sp.get('y')-vicon_data[2])/1000
        z_error = (sp.get('z')-vicon_data[3])/1000
        #yaw_error = -(sp.get('yaw')-(vicon_data[6]*(180/pi))) # Fall back to this one
        yaw_error = sp.get('yaw')+(vicon_data[6]*(180/pi)) # Try this configuration
        if log and log_error : log_data += [x_error,y_error,z_error,yaw_error] # LOG CLUSTER 2
        if log and log_sp : log_data += [sp.get('x')/1000,sp.get('y')/1000,sp.get('z')/1000,sp.get('yaw')*(180/pi)] # LOG CLUSTER 3

        # Get updated control from PID
        pitch = 0
        roll = 0
        yaw = 0
        thrust = pid_thrust.update(z_error) + hover_thrust

        # Thrust compensation
        const = 0.5
        thrust = thrust/(cos(const*pitch*pi/180)*cos(const*roll*pi/180))

        if log and log_cal : log_data += [thrust,pitch,roll,yaw] # LOG CLUSTER 4

        # Set hard cap to output values
        thrust = control.limiter(thrust,thrust_lim[0],thrust_lim[1])
        pitch = control.limiter(pitch,pitchroll_lim[0],pitchroll_lim[1])
        roll = control.limiter(roll,pitchroll_lim[0],pitchroll_lim[1])
        yaw = control.limiter(yaw,yaw_lim[0],yaw_lim[1])
        if log and log_lim : log_data += [thrust,pitch,roll,yaw] # LOG CLUSTER 5


        # Send updated control params
        cf.send_setpoint(roll,pitch,yaw,int(thrust))

        # Save all data to log
        if log : vicon_log.log_data(log_data)

        # Allow other threads to run
        time.sleep(1/(2*vicon_freq)) 
        
if __name__ == '__main__':

    # constans
    hover_thrust = 41323
    vicon_freq = 100

    # Room limit dict
    rl = {
        'x' : {'min':-1500,'max':1500},
        'y' : {'min':-2000,'max':2000},
        'z' : {'min':0,'max':2500},
    }

    # command limits
    thrust_lim      = [10000, 65535]
    pitchroll_lim   = [-40 , 40]
    yaw_lim         = [-360,360]

    # Setup vicon udp reader and logger
    vicon_udp = viconUDP()
    if log : vicon_log = logger("vicon_log")

    #SP loader with path follow
    path = PathFollow(100, "Course_development/courseToFollow.csv")
     
    # setup crazyFlie client
    cf = easyflie()
    cf.send_start_setpoint()

    # Setup PID control for all axes
    pid_thrust = control.PID(30e3,0,17e3)

    # Tells treads to keep running
    running = True

    # Start program threads
    loader = Thread(target=thread_setpoint_loader)
    loader.start()
    time.sleep(0.2)

    # Start all controllers
    CON = [pid_thrust]
    for controller in CON:
        controller.start()

    main = Thread(target=thread_main_loop)
    main.start()

    # Handle program exit correctly
    while 1 :
        try: time.sleep(0.2)
        except KeyboardInterrupt:
            if log : vicon_log.save_file()
            print(">>>> Sending stop command to Crazyflie <<<<")
            cf.send_stop_setpoint()
            running = False
            exit("Exiting program")
