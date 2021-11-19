import time
import controllers as c
import complementary as com

class baroZestimator:
    def __init__(self,avg_len):
        """Estimates z-height from barometric pressure and a running average of an absolute height value

        Args:
            avg_len (int): number of absolute samples to use for moving average
        """
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

class thrust_estimator:
    def __init__(self,K,amount):
        self.baro_est = baroZestimator(amount)
        self.complementary = com.thrust(K)

    def calibrate(self,vicon_udp:function,barometer:float) -> bool:
        if not self.baro_est:
            print("Calibrating barometer at ground level:")
            time.sleep(1)
        self.baro_est.vicon = vicon_udp()[3]
        self.baro_est.baro = barometer
        time.sleep(0.05)
        print(".",end="",flush=True)
        done_status = self.baro_est.takeAverage()
        if done_status:
            return done_status
        else:
            print("Initial calibration complete") 
            return done_status

    def update(self,vicon_available,vicon_data,drone_data):
        if vicon_available:
            self.baro_est.vicon = vicon_data[3]
        if drone_data:
            self.baro_est.baro = drone_data['baro.pressure']
        z_est = self.baro_est.estimate()
        self.complementary.update(z_est,drone_data['acc_z'],drone_data['time'])
    