from pitchRoll_estimator import pitchRoll_estimator
from ComplimentaryThrust import thrust_estimator

class state_estimator:
    def __init__(self, init_pos, vicon_udp, Kx = .34, Ky = .34, Kz_vel = 0.9,Kz_pos = 0.9):
        """
        Initiates the state estimator based on an initial state

        Args:
            init_pos (dict) {'x','y','z','yaw'}
        """

        self.init_pos = init_pos
        self.est_pos = init_pos
        self.xy_estimator = pitchRoll_estimator(init_pos, vicon_udp, Kx, Ky)
        self.z_estimator = thrust_estimator(Kz_vel,Kz_pos,30)
        self.pos = init_pos


    def update(self, vicon_data, drone_data,vicon_available):
        """
        Updates state_estimator based on values from vicon and drone

        Args:
            vicon_data (list) (t,x,y,z,pitch,roll,yaw), 
            drone_data (dict) {'gyro_x','gyro_y','gyro_z','acc_x','acc_y','acc_z', 'time', 'stateEstimate_yaw'},
            vicon_available (bool) True: vicon is available, False: vicon is not available
        """


        #state estimation missing z
        self.est_pos['yaw'] = drone_data['stateEstimate.yaw']
        xy = self.xy_estimator.update(vicon_available,vicon_data,drone_data)
        z  = self.z_estimator.update(vicon_available,vicon_data,drone_data)
        self.est_pos['x'] = xy['x']
        self.est_pos['y'] = xy['y']
        self.est_pos['z'] = z
        
        return self.est_pos

