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
        """Ensures running that the initialized values as well as moving average is taken correctly

        Returns:
            bool: True if calibration is still in progress
        """

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
                self.est_avg = sum(self.average)/len(self.average) + 1 # to avoid div 0 error
                self.est_height = sum(self.height)/len(self.height) + 1 # to avoid div 0 error
           
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
        """Estimates the z-height of the drone based on two previously known heights

        Returns:
            float: estimated height
        """
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
    def __init__(self,k_vel,k_pos,amount):
        self.baro_est = baroZestimator(amount)
        self.complementary = com.thrust(k_vel, k_pos)
        self.started = False
        self.z_est = 0

    def calibrate(self,vicon_udp,barometer:float) -> bool:
        """Does the calibration of the initial point used for the z-estimation

        Args:
            vicon_udp (function): Function that can be called to get the actual-zheight
            barometer (float): Value of barometric reading the given z-height

        Returns:
            bool: True if calibration is still in progress
        """
        if not self.started:
            print("Calibrating barometer at ground level:")
            time.sleep(1)
            self.started = True
        self.baro_est.vicon = vicon_udp()[3]
        self.baro_est.baro = barometer
        time.sleep(0.01)
        print(".",end="",flush=True)
        done_status = self.baro_est.takeAverage()
        if done_status:
            return done_status
        else:
            print("\nInitial calibration complete") 
            return done_status

    def update(self,vicon_available,vicon_data,drone_data):
        """Update complimentary filter position estimation output

        Args:
            vicon_available (bool): Describes wether to use vicon data
            vicon_data (list): Vicon Tracker UDP parameters
            drone_data (dict): Logged data from sensors on-board the drone

        Returns:
            float: Best estimated z-height of drone
        """
        if vicon_available:
            self.baro_est.vicon = vicon_data[3]
        if drone_data:
            try:
                self.baro_est.baro = drone_data['baro.pressure']
                self.z_est = self.baro_est.estimate()
            except KeyError:
                self.baro_est.baro = drone_data['range.zrange']
                self.z_est = self.baro_est.baro
        return self.complementary.update(self.z_est,drone_data,vicon_data,vicon_available)
    