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
        self.baro_lp = None

    def update(self,height,drone_data,vicon_data,vicon_avail):

        # Low-pass filter barometric data
        if not self.baro_lp:
            self.baro_lp = control.cascade(control.low_pass_bi,4,tau=0.02,init_val=height)

        # Retreive time of logged data
        xtime = drone_data.get('time') 

        # ! Only select one of the below
        # ? Combined best estimate
        drone_vel = drone_data.get('stateEstimate.vz')*1000 # [mm/s] Use on-board estimator to prevent wind-up
        delta_speed = drone_data['stateEstimate.az']*9820*(xtime-self.prev_time) # [delta mm/s]
        self.prev_vel = self.comp_vel.update((self.prev_vel + delta_speed),drone_vel) # [mm/s]

        # ? Use on-board velocity estimator only
        # self.prev_vel = drone_data.get('stateEstimate.vz') # Use on-board estimator

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
        # self.prev_vicon_data = vicon_data
        # ! Only select one of the above

        # 2nd integration from velocity to position (anti wind-up by barometer)
        delta_pos = self.prev_vel*(xtime-self.prev_time) # [delta mm]
        self.prev_pos = self.comp_pos.update((self.prev_pos + delta_pos),height)  # [mm]

        self.prev_time = xtime

        return self.prev_pos