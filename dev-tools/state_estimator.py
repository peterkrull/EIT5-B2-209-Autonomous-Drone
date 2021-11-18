from pitchRoll_estimator import pitchRoll_estimator

class state_estimator:
    def __init__(self, init_pos):
        """
        Initiates the state estimator based on an initial state

        Args:
            init_pos (dict) {'x','y','z','yaw'}
        """


        self.init_pos = init_pos
        self.est_pos = init_pos
        self.xy_estimator = pitchRoll_estimator(init_pos)
        self.pos = init_pos


    def update(self, vicon_data, drone_data,vicon_available):
        """
        Updates state_estimator based on values from vicon and drone

        Args:
            vicon_data (list) (t,x,y,z,pitch,roll,yaw), 
            drone_data (dict) {'gyro_x','gyro_y','gyro_z','acc_x','acc_y','acc_z', 'time', 'stateEstimate_yaw'},
            vicon_available (bool) True: vicon is available, False: vicon is not available
        """

        gyro_data = {'x' : drone_data['gyro_x'], 'y' : drone_data['gyro_y'], 'z' : drone_data['gyro_z']}
        acc_data = {'x': drone_data['acc_x'], 'y': drone_data['acc_y'], 'z': drone_data['acc_z']}

        #state estimation missing z
        self.est_pos['yaw'] = drone_data['stateEstimate_yaw']
        xy = self.xy_estimator.update(gyro_data, acc_data,self.pos['yaw'],drone_data['time'])
        self.est_pos['x'] = xy['x']
        #print("x",xy['x'])
        self.est_pos['y'] = xy['y']
        self.est_pos['z'] = vicon_data[3] #update pos using z-estimator
        
        if vicon_available == 1:
            #use vicon to acquire actual position to improve positioning of data.
            pass
        
        return self.est_pos

