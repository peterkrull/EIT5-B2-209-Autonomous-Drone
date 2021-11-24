import json
import time
from json.decoder import JSONDecodeError
from threading import Thread
from math import pi,cos,sin

from state_estimator import state_estimator
from controllers import control
from data_logger import logger
from easyflie import easyflie
from raspberry_socketreader import viconUDP
from path_follow import PathFollow

# Library for data logging
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Enable logs
log = True
log_error = True
log_sp = True
log_cal = True
log_lim = True
log_drone = True
log_estimate = True

# from path_visualizer import path_visualizer
# # Outcommented since Pi wont have display out
# # Thread to allow for visualizing drone flight
# def thread_visualizer():
#     global sp,running
#     visualizer = path_visualizer(sp.path)
#     while running:
#         visualizer.updateFrame(sp)
#         time.sleep(.3)

# Load config from file
def config_load_from_file(filename = "config.json") -> dict:
    try:
        try: return json.load(open(f"dev-tools/{filename}"))
        except FileNotFoundError: return json.load(open(filename))
    except JSONDecodeError:
        exit("Configuration file is corrupt, please check it again.")

# Constantly load setpoint from file
def thread_setpoint_loader():
    global sp,running
    while running:
        try: sp = json.load(open("dev-tools/const_setpoint.json"))
        except FileNotFoundError: sp = json.load(open("const_setpoint.json"))
        time.sleep(0.5)

# Flight path following thread
def thread_setpoint_loader2():
    global sp,running,vicon_data,path
    vicon_data = [0,0,0,0,0,0]
    while running:
        sp = path.getRef(vicon_data) 
        print(sp)
        time.sleep(0.1)

# Logging thread
def thread_drone_log():
    global drone_data, running
    lg_stab = LogConfig(name='category', period_in_ms=10)
    start_time = time.time()
    for entry in conf['drone_log']:
        lg_stab.add_variable(entry,conf['drone_log'][entry]['type'])

    while running:
        with SyncCrazyflie(cf.URI,cf=cf.cf) as scf:
            with SyncLogger(scf, lg_stab) as logger:
                for log_entry in logger:
                    drone_data = log_entry[1]
                    drone_data['time'] = time.time()- start_time
                    if not running: break

# Main program / control loop
def thread_main_loop():
    global sp,running,vicon_data,drone_data

    # Add column title to log file
    if log : col_titles = ['time','x_pos','y_pos','z_pos','x_rot','y_rot','z_rot','delta_time','z_filtered']      # LOG CLUSTER 1
    if log and log_estimate : col_titles += ['x_pos_est','y_pos_est','z_pos_est','z_rot_est']
    if log and log_error : col_titles += ['x_error','y_error','z_error','yaw_error']                              # LOG CLUSTER 2
    if log and log_sp : col_titles += ['x_setpoint','y_setpoint','z_setpoint','yaw_setpoint', 'vicon_available']  # LOG CLUSTER 3
    if log and log_cal : col_titles += ['thrust_cal','pitch_cal','roll_cal','yaw_cal']                            # LOG CLUSTER 4
    if log and log_lim : col_titles += ['thrust_lim','pitch_lim','roll_lim','yaw_lim']                            # LOG CLUSTER 5
    if log and log_drone : col_titles += [conf["drone_log"][entry]['id'] for entry in conf["drone_log"]]          # LOG CLUSTER 6
    if log : vicon_log.log_data(col_titles)
    if log : del col_titles

    position = {}
    estimated_position = {}

    while running:
        # Get vicon data and log it
        pre_time = time.time()
        vicon_data = vicon_udp.getTimestampedData() # fetch vicon data
        if log : log_data = vicon_data # LOG CLUSTER 1
        if log : log_data += [time.time()-pre_time] # LOG CLUSTER 1 

        # Check room limits
        sp['x'] = control.limiter(sp['x'],**conf['room_limits']['x'])
        sp['y'] = control.limiter(sp['y'],**conf['room_limits']['y'])
        sp['z'] = control.limiter(sp['z'],**conf['room_limits']['z'])

        if bool(drone_data):
            estimated_position = state_est.update(vicon_data, drone_data,sp['viconAvailable'])

        if sp['viconAvailable'] == 1:
            #Flight with Vicon
            position['x']   = vicon_data[1]
            position['y']   = vicon_data[2]
            position['z']   = vicon_data[3]  
            position['yaw'] = vicon_data[6]
        else:
            #Flight without Vicon
            position['x']   = estimated_position['x']
            position['y']   = estimated_position['y']
            position['z']   = estimated_position['z'] 
            position['yaw'] = estimated_position['yaw']

        # Calculate error in position and yaw
        x_error_room = (sp.get('x')-position['x'])/1000
        y_error_room = (sp.get('y')-position['y'])/1000
        z_error = (sp.get('z')-position['z'])/1000
        yaw_error = sp.get('yaw')+(position['yaw']*(180/pi)) 

        # Apply filter to temporary z-rotation value
        z_rot_filtered = filter_yaw.update(position['yaw'])
        if log : log_data += [z_rot_filtered] # LOG CLUSTER 1 

        if log and log_estimate: log_data += [estimated_position['x'],estimated_position['y'],estimated_position['z'],estimated_position['yaw']]

        # Allowing for yaw, calculating errors in drones bodyframe
        x_error_drone =  x_error_room * cos(z_rot_filtered) + y_error_room * sin(z_rot_filtered)
        y_error_drone = -x_error_room * sin(z_rot_filtered) + y_error_room * cos(z_rot_filtered)

        if log and log_error : log_data += [x_error_room,y_error_room,z_error,yaw_error] # LOG CLUSTER 2
        if log and log_sp : log_data += [sp.get('x')/1000,sp.get('y')/1000,sp.get('z')/1000,sp.get('yaw')*(180/pi),sp.get('viconAvailable')] # LOG CLUSTER 3

        # Fix yaw error around -180 deg <-> 180 deg crossing
        if yaw_error < -180:
            yaw_error += 360
        elif yaw_error > 180:
            yaw_error -= 360

        # Get updated control from PID
        pitch = pid_pitch.update(y_error_drone)
        roll = pid_roll.update(x_error_drone)
        yaw = pid_yaw.update(yaw_error)
        thrust = pid_thrust.update(z_error) + conf.get("hover_thrust")

        # Thrust compensation
        const = 0.5
        thrust = thrust/(cos(const*pitch*pi/180)*cos(const*roll*pi/180))

        if log and log_cal : log_data += [thrust,pitch,roll,yaw] # LOG CLUSTER 4

        # Set hard cap to output values
        thrust = control.limiter(thrust,**conf['act_limits']['thrust'])
        pitch = control.limiter(pitch,**conf['act_limits']['pitch'])
        roll = control.limiter(roll,**conf['act_limits']['roll'])
        yaw = control.limiter(yaw,**conf['act_limits']['yaw'])

        if log and log_lim : log_data += [thrust,pitch,roll,yaw] # LOG CLUSTER 5

        if log and log_drone : # LOG CLUSTER 6
            if drone_data:
                log_data += [drone_data[x] for x in conf["drone_log"]] 
                drone_data = None
            else:
                log_data += [None for x in conf["drone_log"]] 
            # For MATLAB processing of data, see 'fillmissing' to use this data

        # Send updated control params
        cf.send_setpoint(roll,pitch,yaw,int(thrust))

        # Save all data to log
        if log : vicon_log.log_data(log_data)

        # Allow other threads to run
        time.sleep(1/(3*conf['vicon_freq'])) 
        
if __name__ == '__main__':

    global conf,drone_data,est_position
    conf = config_load_from_file()

    # Setup vicon udp reader and logger
    vicon_udp = viconUDP()
    if log : vicon_log = logger(conf["log_file_name"])

    # Log data from drone
    drone_data = {}

    #SP loader with path follow
    path = PathFollow(conf["course_params"]["check_radius"], conf["course_params"]["file_path"])

    # Setup PID control for all axes
    pid_thrust = control.PID(**conf["pid_vals"]["thrust"])
    pid_pitch = control.PID(**conf["pid_vals"]["pitch"])
    pid_roll = control.PID(**conf["pid_vals"]["roll"])
    pid_yaw = control.PID(**conf["pid_vals"]["yaw"])

    # Setup YAW-axis filter
    if conf["yaw_filter"]["type"] == "roll_avg": # Rolling average
        filter_yaw = control.roll_avg(conf["yaw_filter"]["roll_avg"]["number"])

    elif conf["yaw_filter"]["type"] == "lowpass": # n-order lowpass filter
        filter_yaw = control.cascade(control.low_pass_bi,**conf["yaw_filter"]["lowpass"])

    # Tells treads to keep running
    running = True

    # setup crazyFlie client
    print("Establishing CF connection")
    cf = easyflie()

    # Start drone logger thread
    if log_drone:
        loader = Thread(target=thread_drone_log)
        loader.start()

    # Wait 1 second and initialize
    time.sleep(1)
    cf.send_start_setpoint()
    print("Connection established")
    time.sleep(.4)
    cf.cf.param.set_value("motion.disable", '1')
    print("Flowdeck disabled for onboard kalman filtering")
    time.sleep(.5)

    # State estimator for panic-mode
    init_pos = vicon_udp.getTimestampedData()
    state_est = state_estimator({'x':init_pos[2],'y':init_pos[3],'z':init_pos[4],'yaw':init_pos[6]},init_pos)    

    # Calibrate barometric pressure
    while state_est.z_estimator.calibrate(vicon_udp.getTimestampedData,drone_data['baro.pressure']):
        #Sends setpoints so the drone does not loose connection
        cf.send_setpoint(0,0,0,0)

    # Start program thread
    loader = Thread(target=thread_setpoint_loader2)
    loader.start()
    time.sleep(0.2)

    # Start all controllers
    CON = [pid_thrust,pid_pitch,pid_roll,pid_yaw]
    for controller in CON:
        controller.start()

    # Start main loop thread
    main = Thread(target=thread_main_loop)
    main.start()

    # Handle program exit correctly
    while 1 :
        try: time.sleep(0.2)
        except KeyboardInterrupt:
            print(">>>> Sending stop command to Crazyflie <<<<")
            running = False

            for i in range(5):
                try: 
                    time.sleep(0.05)
                    cf.send_stop_setpoint()
                except: pass
            
            if log : vicon_log.save_file()
            exit("Exiting program")
        except JSONDecodeError: # Does not work, for some reason
            print(">>>> JSON file is corrupted, ending now <<<<")
            sp['x'] = vicon_data[1]
            sp['y'] = vicon_data[2]
            sp['z'] = 500
            time.sleep(1.5)
            sp['z'] = 0
            time.sleep(0.5)
            cf.send_stop_setpoint()
            if log : vicon_log.save_file()
            running = False
            exit("Exiting program")