from complementary import complementary, pitchroll
from math import sin, cos, pi
import time 

class pitchRoll_estimator:
    def __init__(self,pos):
        """
        Initializes pitchRoll_estimator based on an initial position

        Args:
            pos (dict) {'x','y'} Initial position of the drone in the positioning systems reference frame
        """

        self.g = 9.82
        self.start_time = time.time()
        self.prev_update = self.start_time

        pitch_filter = pitchroll(.1,start_time=self.start_time)
        roll_filter = pitchroll(.1,start_time=self.start_time)

        self.filters = {'pitch':pitch_filter, 'roll':roll_filter}
        self.pos = {'x':pos['x'], 'y':pos['y']}
        self.body_vel = {'x':0, 'y':0}

    def __update_bodyAcc(self, gyro,acc,acc_z, t,angle):
        """
        Calculates the acceleration in the bodyframe based on gyro and accelerometer data

        Args:
            gyro (float) rotational speed : unit [rad/s]
            acc  (float) acceleration : unit g [m/s^2]
            acc_z (float) acceleration perpendicular to the drone : unit g [m/s^2]
            t (float) unix time : unit [s]
        """

        est_angle = self.filters[angle].update(gyro,acc,acc_z,t)
        #Currently estimates acceleration using approximation described in report, 
        #if upgrade needed use thrust for more precise calculation
        est_acc = sin(est_angle*pi/180) * self.g 
        return est_acc

    def update(self,gyro,acc,yaw,t):
        """
        Updates the pitchRoll_estimator with coordinates in the inertial frame

        Args:
            gyro (dict) {'x','y'} : unit [rad/s] rotational speed around the different axis
            acc  (dict) {'x','y','z'} : unit g [m/s^2] Acceleration along the different axis
            yaw (float) : unit [degrees] the current yaw of the drone
            t (float) : unit [s] unix time
        """
        #Finds acceleration in the drones body coordinates
        pitch_acc = self.__update_bodyAcc(gyro['x'],acc['x'],acc['z'], t, 'pitch')
        roll_acc = self.__update_bodyAcc(gyro['y'],acc['y'],acc['z'], t, 'roll')

        #Transforms body acceleration to inertial acceleration using rot-matrix
        x_acc = cos(yaw*pi/180)*pitch_acc-sin(yaw*pi/180)*roll_acc
        y_acc = sin(yaw*pi/180)*pitch_acc+cos(yaw*pi/180)*roll_acc

        #Integrates acceleration to acquire velocity
        self.body_vel['x'] += x_acc*(t-self.prev_update)
        self.body_vel['y'] += y_acc*(t-self.prev_update)

        #Multiplys bodyvelocity to acquire distance travelled and add this to position
        self.pos['x'] += self.body_vel['x']*(t-self.prev_update)
        self.pos['y'] += self.body_vel['y']*(t-self.prev_update)

        self.prev_update = t

        return self.pos




