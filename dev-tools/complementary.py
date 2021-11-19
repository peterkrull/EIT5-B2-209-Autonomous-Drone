import time
import numpy

#Complementary filter
class complementary:

    def __init__(self,k):
        self.k = k

    def update(self,data_1,data_2):
        return data_1*self.k + data_2*(1-self.k)

class pitchroll:
    def __init__(self,k):
        self.comp = complementary(k)
        self.prev_gyro = 0.0
        self.prev_time = 0.0
        self.angle = 0.0

    def update(self,gyro,acc,acc_z,time):
        #Calculate delta angel
        xtime = time
        integrate_gyro = (gyro*(180/numpy.pi))*(xtime-self.prev_time)
        self.prev_time = xtime
        
        #self.angle = (180/numpy.pi)*(1-self.k)*numpy.arctan(acc/acc_z)+self.k*(self.prev_gyro+integrate_gyro)
        self.angle = self.comp.update((self.prev_gyro+integrate_gyro),numpy.arctan(acc/acc_z)*(180/numpy.pi))
        self.prev_gyro = self.angle

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