import time
import numpy

#Complementary filter
class complementary:
        def __init__(self,gyro,acc,acc_z,k):
            #For gyro
            self.gyro = gyro
            self.prev_gyro = 0.0
            self.delta_gyro = 0.0
            self.integrate_gyro = 0.0
            self.prev_time = time.time()
            self.gyro_angle_scaled = 0.0

            #For acceleration
            self.acc = acc
            self.acc_z = acc_z
            self.acc_angle_scaled = 0.0

            #Filter scala
            self.k = k

            self.angle = 0.0

        def update(self):
            #Calculate delta angel
            xtime = time.time()
            self.integrate_gyro += (self.gyro*(180/numpy.pi))*(xtime-self.prev_time)
            self.prev_time = xtime
            self.delta_gyro = self.integrate_gyro-self.prev_gyro
            self.prev_gyro = self.integrate_gyro

            #Sumation of delta angle and roll angle
            self.gyro_angle_scaled = (self.delta_gyro+self.angle)*self.k

            #Convert to angle acceleration
            self.acc_angle_scaled = numpy.arctan(self.acc, self.acc_z)*(1-self.k)

            #Sumation of angle acceleration and angle gyro
            self.angle = self.acc_angle_scaled+self.gyro_angle_scaled
            return self.angle




