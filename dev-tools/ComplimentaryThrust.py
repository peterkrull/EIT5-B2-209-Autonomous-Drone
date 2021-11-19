import time
import numpy
import csv
import controllers as c


class baroZestimator:
    def __init__(self,avg_len):
        self.baro, self.vicon = None,None
        self.average, self.height = [],[]
        self.init_avg, self.init_height = None,None
        self.est_avg,self.est_height = None,None
        self.avg_len = avg_len

    def takeAverage(self):
        if self.baro and self.vicon:
            self.average.append(self.baro)
            self.height.append(self.vicon)

        if len(self.average) < self.avg_len and len(self.height) < self.avg_len:
            return True
        if len(self.average) >= self.avg_len and len(self.height) >= self.avg_len:
            if not self.init_avg and not self.init_height:
                self.init_avg = sum(self.average)/len(self.average)
                self.init_height  = sum(self.height)/len(self.height)
            else:
                self.est_avg = sum(self.average)/len(self.average)
                self.est_height  = sum(self.height)/len(self.height)
                self.average.pop(0)
                self.height.pop(0)

    def estimate(self):
        self.takeAverage()
        baroZ_estimate = (((self.est_height-self.init_height)/(self.est_avg-self.init_avg))*(self.average[len(self.average)-1]-self.init_avg) + self.init_height)
        return baroZ_estimate

import random

# Double integration
Dinte = c.control.cascade(c.control.integral,2,K = 1)

# Setup and initial calibration
baro_est = baroZestimator(30)
while baro_est.takeAverage():
    baro_est.vicon = random.randrange(0,10)
    baro_est.baro = random.randrange(0,100)

# Running average
for i in range(100):
    baro_est.vicon = random.randrange(900,1000)
    baro_est.baro = random.randrange(9000,10000)
    print("RUNNING AVG",baro_est.estimate())