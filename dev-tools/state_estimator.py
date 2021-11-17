from _typeshed import Self
from pitchRoll_estimator import pitchRoll_estimator

class state_estimator:
    def __init__(self, init_pos):
        self.est_pos = {'x','y','z'}
        self.xy_estimator = pitchRoll_estimator(init_pos)
        self.pos = {'x','y','z','yaw'}

    def update(self, vicon_data, drone_data):
        gyro_data = {'x' : drone_data['gyro_x'], 'y' : drone_data['gyro_y'], 'z' : drone_data['gyro_z']}
        acc_data = {'x': drone_data['acc_x'], 'y': drone_data['acc_y'], 'z': drone_data['acc_z']}


        if vicon_data['vicon_availabe'] == 1:
            #state estimation missing z
            self.pos['yaw'] = drone_data['stateEstimate_yaw']
            self.pos['x','y'] = self.xy_estimator.update(gyro_data, acc_data,self.yaw)
            self.pos['z'] = vicon_data['z'] #update pos using 

            # update reference position based on vicon
        else:
            #state estimation missing z
            self.xy_estimator.update(self.xy_estimator.update(gyro_data, acc_data,self.yaw))
