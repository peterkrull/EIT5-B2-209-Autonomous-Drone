import time
import numpy

#Complementary filter
class complementary:
        def __init__(self,k):
            #For gyro
            self.prev_gyro = 0.0
            self.prev_time = 0.0
            #Filter scala
            self.k = k
            self.angle = 0.0

        def update(self,gyro,acc,acc_z,time):
            #Calculate delta angel
            xtime = time
            integrate_gyro = (gyro*(180/numpy.pi))*(xtime-self.prev_time)
            self.prev_time = xtime
            
            self.angle = (180/numpy.pi)*(1-self.k)*numpy.arctan(acc/acc_z)+self.k*(self.prev_gyro+integrate_gyro)
            self.prev_gyro = self.angle

            return self.angle
