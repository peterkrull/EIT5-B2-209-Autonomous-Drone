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
        self.latest_baro = None
        self.avg_len = avg_len

    def takeAverage(self):

        # Defind latest barometer measurement
        if self.baro:
            self.latest_baro = self.baro

        # Append to averaging list
        if self.baro and self.vicon:
            self.average.append(self.baro)
            self.height.append(self.vicon)
            self.baro,self.vicon = 0,0

            # Initial average
            if len(self.average) < self.avg_len and len(self.height) < self.avg_len:
                self.init_avg = sum(self.average)/len(self.average)
                self.init_height = sum(self.height)/len(self.height)
                self.est_avg = sum(self.average)/len(self.average) + 1
                self.est_height = sum(self.height)/len(self.height) + 1
           
            # Regular rolling average
            if len(self.average) >= self.avg_len and len(self.height) >= self.avg_len:
                self.est_avg = sum(self.average)/len(self.average)
                self.est_height = sum(self.height)/len(self.height)
                self.average.pop(0)
                self.height.pop(0)

        # For initial calibration, return true to keep loop running
        if len(self.average) < self.avg_len - 1 and len(self.height) < self.avg_len - 1:
            return True

    def estimate(self):
        self.takeAverage()
        #print(f"init baro : {self.init_avg}, init height {self.init_height} : latest baro : {self.est_avg}, latest height {self.est_height}, baro meas: {self.latest_baro}")
        try:
            pressure_gradient = (self.est_height-self.init_height)/(self.est_avg-self.init_avg)
            baroZ_estimate = (pressure_gradient*(self.latest_baro-self.init_avg) + self.init_height)
        except:
            pressure_gradient = 1
            baroZ_estimate = (pressure_gradient*(self.latest_baro-self.init_avg) + self.init_height)

        #print(f"est height {baroZ_estimate}")
        return baroZ_estimate

class thrust_estimator:
    def __init__(self,K,amount):
        self.baro_est = baroZestimator(amount)
        self.complementary = com.thrust(K)
        self.started = False

    def calibrate(self,vicon_udp,barometer:float) -> bool:
        if not self.started:
            print("Calibrating barometer at ground level:")
            time.sleep(1)
            self.started = True
        self.baro_est.vicon = vicon_udp()[3]
        self.baro_est.baro = barometer
        time.sleep(0.05)
        print(".",end="",flush=True)
        done_status = self.baro_est.takeAverage()
        if done_status:
            return done_status
        else:
            print("\nInitial calibration complete") 
            return done_status

    def update(self,vicon_available,vicon_data,drone_data):
        if vicon_available:
            self.baro_est.vicon = vicon_data[3]
        if drone_data:
            self.baro_est.baro = drone_data['baro.pressure']
        z_est = self.baro_est.estimate()
        return self.complementary.update(z_est,drone_data['acc.z'],drone_data['time'])
    