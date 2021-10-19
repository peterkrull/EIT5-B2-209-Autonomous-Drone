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

    setpoint = [-1000,1000,1000]

    # setup crazyFlie client
    cf = easyflie()
    cf.send_start_setpoint()

    try:
        while True:
            vicon_data = vicon_udp.getTimestampedData() # fetch vicon data
            vicon_log.log_data(vicon_data) # save data with timestamp
            vicon_data.pop(0) # remove timestamp from dataset

            # Calculate error in position
            x_error = setpoint[0]-vicon_data[0]
            y_error = setpoint[1]-vicon_data[1]
            y_error = setpoint[2]-vicon_data[2]

            

            # MAIN PROGRAM LOOP
            pass
    except KeyboardInterrupt:
        vicon_log.save_file()

    
