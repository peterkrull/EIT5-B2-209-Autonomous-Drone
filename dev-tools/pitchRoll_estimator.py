from numpy.core.numeric import roll
from complementary import complementary, pitchroll
from math import sin, cos, pi
import time 
#from termcolor import colored

class pitchRoll_estimator:
    def __init__(self,pos,vicon_data,Kx = .34, Ky = .34, flowdeck = False):
        """
        Initializes pitchRoll_estimator based on an initial position

        Args:
            pos (dict) {'x','y'} Initial position of the drone in the positioning systems reference frame
            vicon_data (list) List of positioning data from the vicon system
            Kx (float) Constant for the x-complementary filter
            Ky (float) Constant for the y-complementary filter
            flowdeck (bool) Should the flowdeck be used for positioning, true = yes, false = no
        """

        self.g = 9.82
        self.start_time = 0
        self.prev_update = self.start_time

        pitch_filter = pitchroll(Kx,start_time=self.start_time)
        roll_filter = pitchroll(Ky,start_time=self.start_time)
        self.angle_filters = {'pitch':pitch_filter, 'roll':roll_filter}

        self.flowdeck = flowdeck
        if self.flowdeck == True:
            xb_filter = complementary(.8)
            yb_filter = complementary(.8)
            self.vel_filters = {'xb':xb_filter, 'yb': yb_filter}

        self.pos = {'x':pos['x'], 'y':pos['y']}
        self.body_vel = {'x':0, 'y':0}
        self.inertial_vel = {'x':0, 'y':0}
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
        est_angle = self.angle_filters[angle].update(gyro,acc,acc_z,t)
        #Currently estimates acceleration using approximation described in report, 
        #if upgrade needed use thrust for more precise calculation
        est_acc = sin(est_angle*pi/180) * self.g /drone_mass
    
        self.plot_acc.append(est_acc)
        self.plot_deg.append(est_angle)

        return est_acc
    
    def __flow_to_ms(self, drone_data,direction):
        """
        Calculates the velocity of the drone based on the flow deck data

        Args:
            drone_data (dict) data from the drone containing "motion_deltaX" and "motion_deltaY"
            direction (str) the direction in which the velocity should be calculated ('x' or 'y')
        """
        #don't know how to convert data from the flow deck yet
        #Here is the answer
        #https://fenix.tecnico.ulisboa.pt/downloadFile/1970719973965869/Resumo%20Alargado.pdf
        pass

    def update(self,vicon_available, vicon_data, drone_data):
        """
        Updates the pitchRoll_estimator with coordinates in the inertial frame

        Args:
            vicon_available (bool) is vicon available for positioning (0 = no, 1 = yes)
            vicon_data (list) list of positioning data from the vicon tracker
            drone_data (dict) Dictionary containing the data from the drone
        """
        self.vicon_available = vicon_available

        if self.flowdeck == True:
            if 'motion_deltaX' not in drone_data or 'motion_deltaY' not in drone_data:
                print("drone_data does not contain flow deck data")
                self.flowdeck = False


        gyro = {'x' : drone_data['gyro.x'], 'y' : drone_data['gyro.y']}
        acc = {'x': drone_data['acc.x'], 'y': drone_data['acc.y'], 'z': drone_data['acc.z']}
        yaw = drone_data['stateEstimate.yaw']
        t = drone_data['time']


        #Updates position based on either vicon or onboard sensors depending on availability
        
        #Finds acceleration in the drones body coordinates
        pitch_acc = self.__update_bodyAcc(gyro['x'],acc['x'],acc['z'], t, 'pitch')
        roll_acc = self.__update_bodyAcc(gyro['y'],acc['y'],acc['z'], t, 'roll')

        #Transforms body acceleration to inertial acceleration using rot-matrix
        #x_acc = -1*(cos(yaw*pi/180)*pitch_acc-sin(yaw*pi/180)*roll_acc)
        #y_acc = sin(yaw*pi/180)*pitch_acc+cos(yaw*pi/180)*roll_acc

        #Integrates acceleration to acquire velocity
        #print("delta tid:", t-self.prev_update)
        moment_vel_x = pitch_acc*(t-self.prev_update)
        moment_vel_y = roll_acc*(t-self.prev_update)

        if self.flowdeck == True:
            flow_velx = self.__flow_to_ms(drone_data,'x')
            flow_vely = self.__flow_to_ms(drone_data,'y')

            #self.body_vel['x'] += self.vel_filters['xb'].update(flow_velx, moment_vel_x) 
            moment_vel_x = self.vel_filters['xb'].update(flow_velx, moment_vel_x)
            moment_vel_y = self.vel_filters['yb'].update(flow_vely, moment_vel_y)  

        self.body_vel['x'] += moment_vel_x
        self.body_vel['y'] += moment_vel_y


        self.inertial_vel['x'] = cos(yaw*pi/180)*pitch_acc - sin(yaw*pi/180)*roll_acc
        self.inertial_vel['y'] = sin(yaw*pi/180)*pitch_acc + sin(yaw*pi/180)*roll_acc

        #Multiplys bodyvelocity to acquire distance travelled and add this to position
        body_posChangex = self.inertial_vel['x']*(t-self.prev_update)*1000
        body_posChangey = self.inertial_vel['y']*(t-self.prev_update)*1000
        self.pos['x'] += body_posChangex
        self.pos['y'] += body_posChangey
        
        if vicon_available == 1:
            deltaTime = (vicon_data[0]-self.prev_vicon_data[0])
            viconX = (vicon_data[1]-self.prev_vicon_data[1])/deltaTime/1000
            viconY = (vicon_data[2]-self.prev_vicon_data[2])/deltaTime/1000
            #Differentiates position to acquire velocity
            self.body_vel['x'] = cos(yaw*pi/180)*viconX + sin(yaw*pi/180)*viconY
            self.body_vel['y'] = -sin(yaw*pi/180)*viconX + cos(yaw*pi/180)*viconY

            #Updates position to be vicons position
            self.pos['x'] = vicon_data[1]
            self.pos['y'] = vicon_data[2]

            self.prev_vicon_data = vicon_data

        self.prev_update = t

        return self.pos





