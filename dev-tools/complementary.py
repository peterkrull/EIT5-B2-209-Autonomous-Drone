import time
import math
from controllers import control

#Complementary filter
class complementary:

    def __init__(self,k):
        self.k = k

    def update(self,data_1,data_2):
        return data_1*self.k + data_2*(1-self.k)

    def set_k(self,k):
        self.k = k

class pitchroll:
    def __init__(self,k,start_time = 0):
        self.comp = complementary(k)
        self.prev_gyro = 0.0
        self.prev_time = start_time
        self.angle = 0.0
        self.k = k

    def update(self,gyro,acc,acc_z,time):
        #Calculate delta angel
        xtime = time
        integrate_gyro = (gyro*(180/math.pi))*(xtime-self.prev_time)
        self.prev_time = xtime
        
        self.angle = (1-self.k)*(180/math.pi)*math.atan(acc/acc_z)+self.k*(self.prev_gyro+integrate_gyro)
        #self.angle = self.comp.update((self.prev_gyro+integrate_gyro),math.atan(acc/acc_z)*(180/math.pi))
        self.prev_gyro = self.angle
        return self.angle

class cascaded_complementary_filter_pitchRoll:
    def __init__(self,k,start_time = 0, kp = 25, ki = .01):
        self.comp = complementary(k)
        self.prev_gyro = 0.0
        self.prev_time = start_time
        self.angle = 0.0

        self.PI_filter = control.PID(kp, ki, 0)        
        self.PI_filter.start()

    def update(self,gyro,acc,acc_z,time):
        acc_angle = math.atan(acc/acc_z)*180/math.pi
        print("PI input:", self.angle-acc_angle)
        PI_angle = self.PI_filter.update(self.angle-acc_angle)
        #print("Gyro", gyro,"PI angle", PI_angle)
        angle_vel = gyro-PI_angle

        integrate_gyro = self.prev_gyro+(angle_vel*(180/math.pi))*(time-self.prev_time)

        self.angle = self.comp.update(integrate_gyro, acc_angle)
        #print("Angle", self.angle)
        return self.angle

class thrust:
    def __init__(self,k_vel,k_pos):
        self.k_vel = k_vel
        self.comp_vel = complementary(k_vel)
        self.comp_pos = complementary(k_pos)
        self.prev_vel = 0.0
        self.prev_pos = 0.0
        self.prev_time = 0.0
        self.thrust = 0.0

    def update(self,baro,drone_data,vicon_data,vicon_avail):
        #Calculate double integral of accelerometer data 
        # xtime = time # Original code (May be incorrect)
        # integrate_acc = acc_z*(xtime-self.prev_time)**2
        # self.prev_time = xtime
        
        # self.thrust = self.comp.update((self.prev_acc + integrate_acc),baro)
        # self.prev_acc = self.thrust

        xtime = drone_data.get('time')     

        # ! Only select one of the below
        # ? Use on-board velocity estimator
        self.prev_vel = drone_data.get('stateEstimate.vz') # Use on-board estimator

        # ? Do velocity estimation using Vicon integration
        # integrate_vel = drone_data.get('acc.z')*(xtime-self.prev_time)*9.82
        # vel = (vicon_data[3]-self.prev_vicon_data[3])/(xtime-self.prev_time) # Estimate from vicon
        # # 1st integration from acceleration to velocity (No complimentary!)
        # if vicon_avail:
        #     self.comp_vel.set_k(self.k_vel)
        #     self.prev_vel = self.comp_vel.update((self.prev_vel + integrate_vel),vel)
        # else:
        #     self.comp_vel.set_k(1)
        #     self.prev_vel = self.comp_vel.update((self.prev_vel + integrate_vel),0)
        # ! Only select one of the above

        # 2nd integration from velocity to position
        delta_pos = self.prev_vel*(xtime-self.prev_time)
        self.prev_pos = self.comp_pos.update((self.prev_pos + delta_pos),baro)

        self.prev_time = xtime
        self.prev_vicon_data = vicon_data
        return self.prev_pos