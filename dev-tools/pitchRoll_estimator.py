from complementary import complementary
from math import sin, cos, pi
import time 

class pitchRoll_estimator:
    def __init__(self,pos):
        self.g = 9.82
        self.start_time = time.time()
        self.prev_update = self.start_time

        pitch_filter = complementary(.1,prev_time=self.start_time)
        roll_filter = complementary(.1,prev_time=self.start_time)
        self.filters = {'pitch':pitch_filter, 'roll':roll_filter}
        self.pos = {'x':pos['x'], 'y':pos['y']}
        self.body_vel = {'x':0, 'y':0}

    def update_bodyAcc(self, gyro,acc,acc_z, t,angle):
        est_angle = self.filters[angle].update(gyro,acc,acc_z,t)
        est_acc = sin(est_angle*pi/180) * self.g 
        return est_acc

    def update(self,gyro,acc,yaw,t):
        #Finds acceleration in the drones body coordinates
        pitch_acc = self.update_bodyAcc(gyro['x'],acc['x'],acc['z'], t-self.start_time, 'pitch')
        roll_acc = self.update_bodyAcc(gyro['y'],acc['y'],acc['z'], t-self.start_time, 'roll')

        #Transforms body acceleration to inertial acceleration using rot-matrix
        x_acc = cos(yaw*pi/180)*pitch_acc-sin(yaw*pi/180)*roll_acc
        y_acc = sin(yaw*pi/180)*pitch_acc+cos(yaw*pi/180)*roll_acc

        #Integrates acceleration to acquire velocity
        self.body_vel['x'] += x_acc*(t-self.prev_update)
        self.body_vel['y'] += y_acc*(t-self.prev_update)

        #Integrates velocity to acquire distance travelled
        self.



