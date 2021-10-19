from data_logger import logger
from pid_control import control
from raspberry_socketreader import viconUDP
from easyflie import easyflie

if __name__ == '__main__':

    # Setup vicon udp reader and logger
    vicon_udp = viconUDP()
    vicon_log = logger("vicon_log")

    # Setup PID control for all axes
    pid_thrust = control.PID()
    pid_pitch = control.PID()
    pid_roll = control.PID()
    pid_yaw = control.PID()

    PID = [pid_thrust,pid_pitch,pid_roll,pid_yaw]

    cf = easyflie()

    try:
        while True:
            # MAIN PROGRAM LOOP
            pass
    except KeyboardInterrupt:
        vicon_log.save_file()

    
