import time
import numpy
from controllers import control

#Complementary filter
class complementary:

    def __init__(self,k):
        self.k = k

    def update(self,data_1,data_2):
        return data_1*self.k + data_2*(1-self.k)

class pitchroll:
    def __init__(self,k,start_time = 0):
        self.comp = complementary(k)
        self.prev_gyro = 0.0
        self.prev_time = start_time
        self.angle = 0.0

    def update(self,gyro,acc,acc_z,time):
        #Calculate delta angel
        xtime = time
        integrate_gyro = (gyro*(180/numpy.pi))*(xtime-self.prev_time)
        self.prev_time = xtime
        
        #self.angle = (180/numpy.pi)*(1-self.k)*numpy.arctan(acc/acc_z)+self.k*(self.prev_gyro+integrate_gyro)
        self.angle = self.comp.update((self.prev_gyro-integrate_gyro),numpy.arctan(acc/acc_z)*(180/numpy.pi))
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
        acc_angle = numpy.arctan(acc/acc_z)*180/numpy.pi
        print("PI input:", self.angle-acc_angle)
        PI_angle = self.PI_filter.update(self.angle-acc_angle)
        #print("Gyro", gyro,"PI angle", PI_angle)
        angle_vel = gyro-PI_angle

        integrate_gyro = self.prev_gyro+(angle_vel*(180/numpy.pi))*(time-self.prev_time)

        self.angle = self.comp.update(integrate_gyro, acc_angle)
        #print("Angle", self.angle)
        return self.angle

class thrust:
    def __init__(self,k):
        self.comp = complementary(k)
        self.prev_acc = 0.0
        self.prev_time = 0.0
        self.thrust = 0.0

    def update(self,baro,acc_z,time):
        #Calculate integral of accelerometer data 
        xtime = time
        integrate_acc = acc_z*(xtime-self.prev_time)**2
        self.prev_time = xtime
        
        self.thrust = self.comp.update(baro,(self.prev_acc + integrate_acc))
        self.prev_acc = self.thrust

        return self.thrust