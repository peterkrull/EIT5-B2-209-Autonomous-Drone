from complementary import complementary, pitchroll
from math import sin, cos, pi
import time 
#from termcolor import colored

class pitchRoll_estimator:
    def __init__(self,pos,vicon_data,Kx = .34, Ky = .34):
        """
        Initializes pitchRoll_estimator based on an initial position

        Args:
            pos (dict) {'x','y'} Initial position of the drone in the positioning systems reference frame
        """

        self.g = 9.82
        self.start_time = 0
        self.prev_update = self.start_time

        pitch_filter = pitchroll(Kx,start_time=self.start_time)
        roll_filter = pitchroll(Ky,start_time=self.start_time)

        self.filters = {'pitch':pitch_filter, 'roll':roll_filter}
        self.pos = {'x':pos['x'], 'y':pos['y']}
        self.body_vel = {'x':0, 'y':0}
        self.prev_vicon_data = vicon_data

        self.plot_acc = []
        self.plot_deg = []
        self.plot_time = []

    def __update_bodyAcc(self, gyro,acc,acc_z, t,angle):
        """
        Calculates the acceleration in the bodyframe based on gyro and accelerometer data

        Args:
            gyro (float) rotational speed : unit [rad/s]
            acc  (float) acceleration : unit g [m/s^2]
            acc_z (float) acceleration perpendicular to the drone : unit g [m/s^2]
            t (float) unix time : unit [s]
        """
        drone_mass = 0.0318
        est_angle = self.filters[angle].update(gyro,acc,acc_z,t)
        #Currently estimates acceleration using approximation described in report, 
        #if upgrade needed use thrust for more precise calculation
        est_acc = sin(est_angle*pi/180) * self.g /drone_mass
    
        self.plot_acc.append(est_acc)
        self.plot_deg.append(est_angle)

        return est_acc

    def update(self,vicon_available, vicon_data, gyro,acc,yaw,t):
        """
        Updates the pitchRoll_estimator with coordinates in the inertial frame

        Args:
            gyro (dict) {'x','y'} : unit [rad/s] rotational speed around the different axis
            acc  (dict) {'x','y','z'} : unit g [m/s^2] Acceleration along the different axis
            yaw (float) : unit [degrees] the current yaw of the drone
            t (float) : unit [s] unix time
        """
        self.vicon_available = vicon_available
        #Updates position based on either vicon or onboard sensors depending on availability
        
        #Finds acceleration in the drones body coordinates
        pitch_acc = self.__update_bodyAcc(gyro['x'],acc['x'],acc['z'], t, 'pitch')
        roll_acc = self.__update_bodyAcc(gyro['y'],acc['y'],acc['z'], t, 'roll')

        #Transforms body acceleration to inertial acceleration using rot-matrix
        x_acc = -1*(cos(yaw*pi/180)*pitch_acc-sin(yaw*pi/180)*roll_acc)
        y_acc = sin(yaw*pi/180)*pitch_acc+cos(yaw*pi/180)*roll_acc

        #Integrates acceleration to acquire velocity
        #print("delta tid:", t-self.prev_update)
        self.body_vel['x'] += x_acc*(t-self.prev_update)
        self.body_vel['y'] += y_acc*(t-self.prev_update)

        #Multiplys bodyvelocity to acquire distance travelled and add this to position
        body_posChangex = self.body_vel['x']*(t-self.prev_update)*1000
        body_posChangey = self.body_vel['y']*(t-self.prev_update)*1000
        self.pos['x'] += body_posChangex
        self.pos['y'] += body_posChangey
        
        if vicon_available == 1:
            deltaTime = (vicon_data[0]-self.prev_vicon_data[0])
            #Differentiates position to acquire velocity
            self.body_vel['x'] = (vicon_data[1]-self.prev_vicon_data[1])/deltaTime/1000
            self.body_vel['y'] = (vicon_data[2]-self.prev_vicon_data[2])/deltaTime/1000

            #Updates position to be vicons position
            self.pos['x'] = vicon_data[1]
            self.pos['y'] = vicon_data[2]

            self.prev_vicon_data = vicon_data

        self.prev_update = t

        return self.pos




